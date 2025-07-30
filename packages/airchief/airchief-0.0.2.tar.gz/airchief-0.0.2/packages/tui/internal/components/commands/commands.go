package commands

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/compat"
	"github.com/shaneholloman/airchief/internal/app"
	"github.com/shaneholloman/airchief/internal/commands"
	"github.com/shaneholloman/airchief/internal/layout"
	"github.com/shaneholloman/airchief/internal/styles"
	"github.com/shaneholloman/airchief/internal/theme"
)

type CommandsComponent interface {
	tea.Model
	tea.ViewModel
	layout.Sizeable
	SetBackgroundColor(color compat.AdaptiveColor)
}

type commandsComponent struct {
	app           *app.App
	width, height int
	showKeybinds  bool
	background    *compat.AdaptiveColor
	limit         *int
}

func (c *commandsComponent) SetSize(width, height int) tea.Cmd {
	c.width = width
	c.height = height
	return nil
}

func (c *commandsComponent) GetSize() (int, int) {
	return c.width, c.height
}

func (c *commandsComponent) SetBackgroundColor(color compat.AdaptiveColor) {
	c.background = &color
}

func (c *commandsComponent) Init() tea.Cmd {
	return nil
}

func (c *commandsComponent) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		c.width = msg.Width
		c.height = msg.Height
	}
	return c, nil
}

func (c *commandsComponent) View() string {
	t := theme.CurrentTheme()

	triggerStyle := lipgloss.NewStyle().
		Foreground(t.Primary()).
		Bold(true)

	descriptionStyle := lipgloss.NewStyle().
		Foreground(t.Text())

	keybindStyle := lipgloss.NewStyle().
		Foreground(t.TextMuted())

	if c.background != nil {
		triggerStyle = triggerStyle.Background(*c.background)
		descriptionStyle = descriptionStyle.Background(*c.background)
		keybindStyle = keybindStyle.Background(*c.background)
	}

	var commandsWithTriggers []commands.Command
	for _, cmd := range c.app.Commands.Sorted() {
		if cmd.Trigger != "" {
			commandsWithTriggers = append(commandsWithTriggers, cmd)
		}
	}
	if c.limit != nil && len(commandsWithTriggers) > *c.limit {
		commandsWithTriggers = commandsWithTriggers[:*c.limit]
	}

	if len(commandsWithTriggers) == 0 {
		return styles.Muted().Render("No commands with triggers available")
	}

	// Calculate column widths
	maxTriggerWidth := 0
	maxDescriptionWidth := 0
	maxKeybindWidth := 0

	// Prepare command data
	type commandRow struct {
		trigger     string
		description string
		keybinds    string
	}

	rows := make([]commandRow, 0, len(commandsWithTriggers))

	for _, cmd := range commandsWithTriggers {
		trigger := "/" + cmd.Trigger
		description := cmd.Description

		// Format keybindings
		var keybindStrs []string
		if c.showKeybinds {
			for _, kb := range cmd.Keybindings {
				if kb.RequiresLeader {
					keybindStrs = append(keybindStrs, *c.app.Config.Keybinds.Leader+" "+kb.Key)
				} else {
					keybindStrs = append(keybindStrs, kb.Key)
				}
			}
		}
		keybinds := strings.Join(keybindStrs, ", ")

		rows = append(rows, commandRow{
			trigger:     trigger,
			description: description,
			keybinds:    keybinds,
		})

		// Update max widths
		if len(trigger) > maxTriggerWidth {
			maxTriggerWidth = len(trigger)
		}
		if len(description) > maxDescriptionWidth {
			maxDescriptionWidth = len(description)
		}
		if len(keybinds) > maxKeybindWidth {
			maxKeybindWidth = len(keybinds)
		}
	}

	// Add padding between columns
	columnPadding := 3

	// Build the output
	var output strings.Builder

	for _, row := range rows {
		// Pad each column to align properly
		trigger := fmt.Sprintf("%-*s", maxTriggerWidth, row.trigger)
		description := fmt.Sprintf("%-*s", maxDescriptionWidth, row.description)

		// Apply styles and combine
		line := triggerStyle.Render(trigger) +
			triggerStyle.Render(strings.Repeat(" ", columnPadding)) +
			descriptionStyle.Render(description)

		if c.showKeybinds && row.keybinds != "" {
			line += keybindStyle.Render(strings.Repeat(" ", columnPadding)) +
				keybindStyle.Render(row.keybinds)
		}

		output.WriteString(line + "\n")
	}

	// Remove trailing newline
	result := strings.TrimSuffix(output.String(), "\n")

	return result
}

type Option func(*commandsComponent)

func WithKeybinds(show bool) Option {
	return func(c *commandsComponent) {
		c.showKeybinds = show
	}
}

func WithBackground(background compat.AdaptiveColor) Option {
	return func(c *commandsComponent) {
		c.background = &background
	}
}

func WithLimit(limit int) Option {
	return func(c *commandsComponent) {
		c.limit = &limit
	}
}

func New(app *app.App, opts ...Option) CommandsComponent {
	c := &commandsComponent{
		app:          app,
		background:   nil,
		showKeybinds: true,
	}
	for _, opt := range opts {
		opt(c)
	}
	return c
}
