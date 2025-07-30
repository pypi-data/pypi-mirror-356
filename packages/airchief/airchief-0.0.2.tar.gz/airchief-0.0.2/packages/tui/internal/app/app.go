package app

import (
	"context"
	"fmt"
	"path/filepath"
	"sort"
	"strings"

	"log/slog"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/shaneholloman/airchief/internal/commands"
	"github.com/shaneholloman/airchief/internal/config"
	"github.com/shaneholloman/airchief/internal/theme"
	"github.com/shaneholloman/airchief/internal/util"
	"github.com/shaneholloman/airchief/pkg/client"
)

var RootPath string

type App struct {
	Info      client.AppInfo
	Version   string
	StatePath string
	Config    *client.ConfigInfo
	Client    *client.ClientWithResponses
	State     *config.State
	Provider  *client.ProviderInfo
	Model     *client.ModelInfo
	Session   *client.SessionInfo
	Messages  []client.MessageInfo
	Commands  commands.CommandRegistry
}

type SessionSelectedMsg = *client.SessionInfo
type ModelSelectedMsg struct {
	Provider client.ProviderInfo
	Model    client.ModelInfo
}
type SessionClearedMsg struct{}
type CompactSessionMsg struct{}
type SendMsg struct {
	Text        string
	Attachments []Attachment
}
type CompletionDialogTriggerdMsg struct {
	InitialValue string
}

func New(
	ctx context.Context,
	version string,
	appInfo client.AppInfo,
	httpClient *client.ClientWithResponses,
) (*App, error) {
	RootPath = appInfo.Path.Root

	configResponse, err := httpClient.PostConfigGetWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	configInfo := configResponse.JSON200
	if configInfo.Keybinds == nil {
		leader := "ctrl+x"
		keybinds := client.ConfigKeybinds{
			Leader: &leader,
		}
		configInfo.Keybinds = &keybinds
	}

	appStatePath := filepath.Join(appInfo.Path.State, "tui")
	appState, err := config.LoadState(appStatePath)
	if err != nil {
		appState = config.NewState()
		config.SaveState(appStatePath, appState)
	}

	if configInfo.Theme != nil {
		appState.Theme = *configInfo.Theme
	}
	if configInfo.Model != nil {
		splits := strings.Split(*configInfo.Model, "/")
		appState.Provider = splits[0]
		appState.Model = strings.Join(splits[1:], "/")
	}

	if appState.Theme != "" {
		theme.SetTheme(appState.Theme)
	}

	slog.Debug("Loaded config", "config", configInfo)

	app := &App{
		Info:      appInfo,
		Version:   version,
		StatePath: appStatePath,
		Config:    configInfo,
		State:     appState,
		Client:    httpClient,
		Session:   &client.SessionInfo{},
		Messages:  []client.MessageInfo{},
		Commands:  commands.LoadFromConfig(configInfo),
	}

	return app, nil
}

func (a *App) InitializeProvider() tea.Cmd {
	return func() tea.Msg {
		providersResponse, err := a.Client.PostProviderListWithResponse(context.Background())
		if err != nil {
			slog.Error("Failed to list providers", "error", err)
			// TODO: notify user
			return nil
		}
		providers := []client.ProviderInfo{}
		var defaultProvider *client.ProviderInfo
		var defaultModel *client.ModelInfo

		var anthropic *client.ProviderInfo
		for _, provider := range providersResponse.JSON200.Providers {
			if provider.Id == "anthropic" {
				anthropic = &provider
			}
		}

		// default to anthropic if available
		if anthropic != nil {
			defaultProvider = anthropic
			defaultModel = getDefaultModel(providersResponse, *anthropic)
		}

		for _, provider := range providersResponse.JSON200.Providers {
			if defaultProvider == nil || defaultModel == nil {
				defaultProvider = &provider
				defaultModel = getDefaultModel(providersResponse, provider)
			}
			providers = append(providers, provider)
		}
		if len(providers) == 0 {
			slog.Error("No providers configured")
			return nil
		}

		var currentProvider *client.ProviderInfo
		var currentModel *client.ModelInfo
		for _, provider := range providers {
			if provider.Id == a.State.Provider {
				currentProvider = &provider

				for _, model := range provider.Models {
					if model.Id == a.State.Model {
						currentModel = &model
					}
				}
			}
		}
		if currentProvider == nil || currentModel == nil {
			currentProvider = defaultProvider
			currentModel = defaultModel
		}

		// TODO: handle no provider or model setup, yet
		return ModelSelectedMsg{
			Provider: *currentProvider,
			Model:    *currentModel,
		}
	}
}

func getDefaultModel(response *client.PostProviderListResponse, provider client.ProviderInfo) *client.ModelInfo {
	if match, ok := response.JSON200.Default[provider.Id]; ok {
		model := provider.Models[match]
		return &model
	} else {
		for _, model := range provider.Models {
			return &model
		}
	}
	return nil
}

type Attachment struct {
	FilePath string
	FileName string
	MimeType string
	Content  []byte
}

func (a *App) IsBusy() bool {
	if len(a.Messages) == 0 {
		return false
	}

	lastMessage := a.Messages[len(a.Messages)-1]
	return lastMessage.Metadata.Time.Completed == nil
}

func (a *App) SaveState() {
	err := config.SaveState(a.StatePath, a.State)
	if err != nil {
		slog.Error("Failed to save state", "error", err)
	}
}

func (a *App) InitializeProject(ctx context.Context) tea.Cmd {
	cmds := []tea.Cmd{}

	session, err := a.CreateSession(ctx)
	if err != nil {
		// status.Error(err.Error())
		return nil
	}

	a.Session = session
	cmds = append(cmds, util.CmdHandler(SessionSelectedMsg(session)))

	go func() {
		response, err := a.Client.PostSessionInitialize(ctx, client.PostSessionInitializeJSONRequestBody{
			SessionID:  a.Session.Id,
			ProviderID: a.Provider.Id,
			ModelID:    a.Model.Id,
		})
		if err != nil {
			slog.Error("Failed to initialize project", "error", err)
			// status.Error(err.Error())
		}
		if response != nil && response.StatusCode != 200 {
			slog.Error("Failed to initialize project", "error", response.StatusCode)
			// status.Error(fmt.Sprintf("failed to initialize project: %d", response.StatusCode))
		}
	}()

	return tea.Batch(cmds...)
}

func (a *App) CompactSession(ctx context.Context) tea.Cmd {
	response, err := a.Client.PostSessionSummarizeWithResponse(ctx, client.PostSessionSummarizeJSONRequestBody{
		SessionID:  a.Session.Id,
		ProviderID: a.Provider.Id,
		ModelID:    a.Model.Id,
	})
	if err != nil {
		slog.Error("Failed to compact session", "error", err)
	}
	if response != nil && response.StatusCode() != 200 {
		slog.Error("Failed to compact session", "error", response.StatusCode)
	}
	return nil
}

func (a *App) MarkProjectInitialized(ctx context.Context) error {
	response, err := a.Client.PostAppInitialize(ctx)
	if err != nil {
		slog.Error("Failed to mark project as initialized", "error", err)
		return err
	}
	if response != nil && response.StatusCode != 200 {
		return fmt.Errorf("failed to initialize project: %d", response.StatusCode)
	}
	return nil
}

func (a *App) CreateSession(ctx context.Context) (*client.SessionInfo, error) {
	resp, err := a.Client.PostSessionCreateWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if resp != nil && resp.StatusCode() != 200 {
		return nil, fmt.Errorf("failed to create session: %d", resp.StatusCode())
	}
	session := resp.JSON200
	return session, nil
}

func (a *App) SendChatMessage(ctx context.Context, text string, attachments []Attachment) tea.Cmd {
	var cmds []tea.Cmd
	if a.Session.Id == "" {
		session, err := a.CreateSession(ctx)
		if err != nil {
			// status.Error(err.Error())
			return nil
		}
		a.Session = session
		cmds = append(cmds, util.CmdHandler(SessionSelectedMsg(session)))
	}

	// TODO: Handle attachments when API supports them
	if len(attachments) > 0 {
		// For now, ignore attachments
		// return "", fmt.Errorf("attachments not supported yet")
	}

	part := client.MessagePart{}
	part.FromMessagePartText(client.MessagePartText{
		Type: "text",
		Text: text,
	})
	parts := []client.MessagePart{part}

	go func() {
		response, err := a.Client.PostSessionChat(ctx, client.PostSessionChatJSONRequestBody{
			SessionID:  a.Session.Id,
			Parts:      parts,
			ProviderID: a.Provider.Id,
			ModelID:    a.Model.Id,
		})
		if err != nil {
			slog.Error("Failed to send message", "error", err)
			// status.Error(err.Error())
		}
		if response != nil && response.StatusCode != 200 {
			slog.Error("Failed to send message", "error", fmt.Sprintf("failed to send message: %d", response.StatusCode))
			// status.Error(fmt.Sprintf("failed to send message: %d", response.StatusCode))
		}
	}()

	// The actual response will come through SSE
	// For now, just return success
	return tea.Batch(cmds...)
}

func (a *App) Cancel(ctx context.Context, sessionID string) error {
	response, err := a.Client.PostSessionAbort(ctx, client.PostSessionAbortJSONRequestBody{
		SessionID: sessionID,
	})
	if err != nil {
		slog.Error("Failed to cancel session", "error", err)
		// status.Error(err.Error())
		return err
	}
	if response != nil && response.StatusCode != 200 {
		slog.Error("Failed to cancel session", "error", fmt.Sprintf("failed to cancel session: %d", response.StatusCode))
		// status.Error(fmt.Sprintf("failed to cancel session: %d", response.StatusCode))
		return fmt.Errorf("failed to cancel session: %d", response.StatusCode)
	}
	return nil
}

func (a *App) ListSessions(ctx context.Context) ([]client.SessionInfo, error) {
	resp, err := a.Client.PostSessionListWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("failed to list sessions: %d", resp.StatusCode())
	}
	if resp.JSON200 == nil {
		return []client.SessionInfo{}, nil
	}
	sessions := *resp.JSON200

	sort.Slice(sessions, func(i, j int) bool {
		return sessions[i].Time.Created-sessions[j].Time.Created > 0
	})

	return sessions, nil
}

func (a *App) ListMessages(ctx context.Context, sessionId string) ([]client.MessageInfo, error) {
	resp, err := a.Client.PostSessionMessagesWithResponse(ctx, client.PostSessionMessagesJSONRequestBody{SessionID: sessionId})
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("failed to list messages: %d", resp.StatusCode())
	}
	if resp.JSON200 == nil {
		return []client.MessageInfo{}, nil
	}
	messages := *resp.JSON200
	return messages, nil
}

func (a *App) ListProviders(ctx context.Context) ([]client.ProviderInfo, error) {
	resp, err := a.Client.PostProviderListWithResponse(ctx)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("failed to list sessions: %d", resp.StatusCode())
	}
	if resp.JSON200 == nil {
		return []client.ProviderInfo{}, nil
	}

	providers := *resp.JSON200
	return providers.Providers, nil
}

// func (a *App) loadCustomKeybinds() {
//
// }
