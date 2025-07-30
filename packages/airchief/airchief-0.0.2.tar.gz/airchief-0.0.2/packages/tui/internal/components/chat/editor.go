package chat

import (
	"fmt"
	"log/slog"
	"strings"

	"github.com/charmbracelet/bubbles/v2/spinner"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/shaneholloman/airchief/internal/app"
	"github.com/shaneholloman/airchief/internal/commands"
	"github.com/shaneholloman/airchief/internal/components/dialog"
	"github.com/shaneholloman/airchief/internal/components/textarea"
	"github.com/shaneholloman/airchief/internal/image"
	"github.com/shaneholloman/airchief/internal/layout"
	"github.com/shaneholloman/airchief/internal/styles"
	"github.com/shaneholloman/airchief/internal/theme"
	"github.com/shaneholloman/airchief/internal/util"
)

type EditorComponent interface {
	tea.Model
	tea.ViewModel
	layout.Sizeable
	Content() string
	Lines() int
	Value() string
	Submit() (tea.Model, tea.Cmd)
	Clear() (tea.Model, tea.Cmd)
	Paste() (tea.Model, tea.Cmd)
	Newline() (tea.Model, tea.Cmd)
	Previous() (tea.Model, tea.Cmd)
	Next() (tea.Model, tea.Cmd)
}

type editorComponent struct {
	app            *app.App
	width, height  int
	textarea       textarea.Model
	attachments    []app.Attachment
	history        []string
	historyIndex   int
	currentMessage string
	spinner        spinner.Model
}

func (m *editorComponent) Init() tea.Cmd {
	return tea.Batch(textarea.Blink, m.spinner.Tick, tea.EnableReportFocus)
}

func (m *editorComponent) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case spinner.TickMsg:
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd
	case tea.KeyPressMsg:
		// Maximize editor responsiveness for printable characters
		if msg.Text != "" {
			m.textarea, cmd = m.textarea.Update(msg)
			cmds = append(cmds, cmd)
			return m, tea.Batch(cmds...)
		}
	case dialog.ThemeSelectedMsg:
		m.textarea = createTextArea(&m.textarea)
		m.spinner = createSpinner()
		return m, tea.Batch(m.spinner.Tick, textarea.Blink)
	case dialog.CompletionSelectedMsg:
		if msg.IsCommand {
			commandName := strings.TrimPrefix(msg.CompletionValue, "/")
			updated, cmd := m.Clear()
			m = updated.(*editorComponent)
			cmds = append(cmds, cmd)
			cmds = append(cmds, util.CmdHandler(commands.ExecuteCommandMsg(m.app.Commands[commands.CommandName(commandName)])))
			return m, tea.Batch(cmds...)
		} else {
			existingValue := m.textarea.Value()
			modifiedValue := strings.Replace(existingValue, msg.SearchString, msg.CompletionValue, 1)
			m.textarea.SetValue(modifiedValue + " ")
			return m, nil
		}
	}

	m.spinner, cmd = m.spinner.Update(msg)
	cmds = append(cmds, cmd)

	m.textarea, cmd = m.textarea.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}

func (m *editorComponent) Content() string {
	t := theme.CurrentTheme()
	base := styles.BaseStyle().Background(t.Background()).Render
	muted := styles.Muted().Background(t.Background()).Render
	promptStyle := lipgloss.NewStyle().
		Padding(0, 0, 0, 1).
		Bold(true).
		Foreground(t.Primary())
	prompt := promptStyle.Render(">")

	textarea := lipgloss.JoinHorizontal(
		lipgloss.Top,
		prompt,
		m.textarea.View(),
	)
	textarea = styles.BaseStyle().
		Width(m.width).
		PaddingTop(1).
		PaddingBottom(1).
		Background(t.BackgroundElement()).
		Render(textarea)

	hint := base("enter") + muted(" send   ")
	if m.app.IsBusy() {
		hint = muted("working") + m.spinner.View() + muted("  ") + base("esc") + muted(" interrupt")
	}

	model := ""
	if m.app.Model != nil {
		model = muted(m.app.Provider.Name) + base(" "+m.app.Model.Name)
	}

	space := m.width - 2 - lipgloss.Width(model) - lipgloss.Width(hint)
	spacer := lipgloss.NewStyle().Background(t.Background()).Width(space).Render("")

	info := hint + spacer + model
	info = styles.Padded().Background(t.Background()).Render(info)

	content := strings.Join([]string{"", textarea, info}, "\n")
	return content
}

func (m *editorComponent) View() string {
	if m.Lines() > 1 {
		return ""
	}
	return m.Content()
}

func (m *editorComponent) GetSize() (width, height int) {
	return m.width, m.height
}

func (m *editorComponent) SetSize(width, height int) tea.Cmd {
	m.width = width
	m.height = height
	m.textarea.SetWidth(width - 5) // account for the prompt and padding right
	// m.textarea.SetHeight(height - 4)
	return nil
}

func (m *editorComponent) Lines() int {
	return m.textarea.LineCount()
}

func (m *editorComponent) Value() string {
	return m.textarea.Value()
}

func (m *editorComponent) Submit() (tea.Model, tea.Cmd) {
	value := strings.TrimSpace(m.Value())
	if value == "" {
		return m, nil
	}
	if len(value) > 0 && value[len(value)-1] == '\\' {
		// If the last character is a backslash, remove it and add a newline
		m.textarea.SetValue(value[:len(value)-1] + "\n")
		return m, nil
	}

	var cmds []tea.Cmd
	updated, cmd := m.Clear()
	m = updated.(*editorComponent)
	cmds = append(cmds, cmd)

	attachments := m.attachments

	// Save to history if not empty and not a duplicate of the last entry
	if value != "" {
		if len(m.history) == 0 || m.history[len(m.history)-1] != value {
			m.history = append(m.history, value)
		}
		m.historyIndex = len(m.history)
		m.currentMessage = ""
	}

	m.attachments = nil

	cmds = append(cmds, util.CmdHandler(app.SendMsg{Text: value, Attachments: attachments}))
	return m, tea.Batch(cmds...)
}

func (m *editorComponent) Clear() (tea.Model, tea.Cmd) {
	m.textarea.Reset()
	return m, nil
}

func (m *editorComponent) Paste() (tea.Model, tea.Cmd) {
	imageBytes, text, err := image.GetImageFromClipboard()
	if err != nil {
		slog.Error(err.Error())
		return m, nil
	}
	if len(imageBytes) != 0 {
		attachmentName := fmt.Sprintf("clipboard-image-%d", len(m.attachments))
		attachment := app.Attachment{FilePath: attachmentName, FileName: attachmentName, Content: imageBytes, MimeType: "image/png"}
		m.attachments = append(m.attachments, attachment)
	} else {
		m.textarea.SetValue(m.textarea.Value() + text)
	}
	return m, nil
}

func (m *editorComponent) Newline() (tea.Model, tea.Cmd) {
	m.textarea.Newline()
	return m, nil
}

func (m *editorComponent) Previous() (tea.Model, tea.Cmd) {
	currentLine := m.textarea.Line()

	// Only navigate history if we're at the first line
	if currentLine == 0 && len(m.history) > 0 {
		// Save current message if we're just starting to navigate
		if m.historyIndex == len(m.history) {
			m.currentMessage = m.textarea.Value()
		}

		// Go to previous message in history
		if m.historyIndex > 0 {
			m.historyIndex--
			m.textarea.SetValue(m.history[m.historyIndex])
		}
		return m, nil
	}
	return m, nil
}

func (m *editorComponent) Next() (tea.Model, tea.Cmd) {
	currentLine := m.textarea.Line()
	value := m.textarea.Value()
	lines := strings.Split(value, "\n")
	totalLines := len(lines)

	// Only navigate history if we're at the last line
	if currentLine == totalLines-1 {
		if m.historyIndex < len(m.history)-1 {
			// Go to next message in history
			m.historyIndex++
			m.textarea.SetValue(m.history[m.historyIndex])
		} else if m.historyIndex == len(m.history)-1 {
			// Return to the current message being composed
			m.historyIndex = len(m.history)
			m.textarea.SetValue(m.currentMessage)
		}
		return m, nil
	}
	return m, nil
}

func createTextArea(existing *textarea.Model) textarea.Model {
	t := theme.CurrentTheme()
	bgColor := t.BackgroundElement()
	textColor := t.Text()
	textMutedColor := t.TextMuted()

	ta := textarea.New()

	ta.Styles.Blurred.Base = lipgloss.NewStyle().Background(bgColor).Foreground(textColor)
	ta.Styles.Blurred.CursorLine = lipgloss.NewStyle().Background(bgColor)
	ta.Styles.Blurred.Placeholder = lipgloss.NewStyle().Background(bgColor).Foreground(textMutedColor)
	ta.Styles.Blurred.Text = lipgloss.NewStyle().Background(bgColor).Foreground(textColor)
	ta.Styles.Focused.Base = lipgloss.NewStyle().Background(bgColor).Foreground(textColor)
	ta.Styles.Focused.CursorLine = lipgloss.NewStyle().Background(bgColor)
	ta.Styles.Focused.Placeholder = lipgloss.NewStyle().Background(bgColor).Foreground(textMutedColor)
	ta.Styles.Focused.Text = lipgloss.NewStyle().Background(bgColor).Foreground(textColor)
	ta.Styles.Cursor.Color = t.Primary()

	ta.Prompt = " "
	ta.ShowLineNumbers = false
	ta.CharLimit = -1

	if existing != nil {
		ta.SetValue(existing.Value())
		ta.SetWidth(existing.Width())
		ta.SetHeight(existing.Height())
	}

	ta.Focus()
	return ta
}

func createSpinner() spinner.Model {
	return spinner.New(
		spinner.WithSpinner(spinner.Ellipsis),
		spinner.WithStyle(
			styles.
				Muted().
				Background(theme.CurrentTheme().Background()).
				Width(3)),
	)
}

func NewEditorComponent(app *app.App) EditorComponent {
	s := createSpinner()
	ta := createTextArea(nil)

	return &editorComponent{
		app:            app,
		textarea:       ta,
		history:        []string{},
		historyIndex:   0,
		currentMessage: "",
		spinner:        s,
	}
}
