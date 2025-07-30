package main

import (
	"context"
	"encoding/json"
	"log/slog"
	"os"
	"path/filepath"
	"strings"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/shaneholloman/airchief/internal/app"
	"github.com/shaneholloman/airchief/internal/tui"
	"github.com/shaneholloman/airchief/pkg/client"
)

var Version = "dev"

func main() {
	version := Version
	if version != "dev" && !strings.HasPrefix(Version, "v") {
		version = "v" + Version
	}

	url := os.Getenv("AIRCHIEF_SERVER")

	appInfoStr := os.Getenv("AIRCHIEF_APP_INFO")
	var appInfo client.AppInfo
	json.Unmarshal([]byte(appInfoStr), &appInfo)

	logfile := filepath.Join(appInfo.Path.Data, "log", "tui.log")
	if _, err := os.Stat(filepath.Dir(logfile)); os.IsNotExist(err) {
		err := os.MkdirAll(filepath.Dir(logfile), 0755)
		if err != nil {
			slog.Error("Failed to create log directory", "error", err)
			os.Exit(1)
		}
	}
	file, err := os.Create(logfile)
	if err != nil {
		slog.Error("Failed to create log file", "error", err)
		os.Exit(1)
	}
	defer file.Close()
	logger := slog.New(slog.NewTextHandler(file, &slog.HandlerOptions{Level: slog.LevelDebug}))
	slog.SetDefault(logger)

	httpClient, err := client.NewClientWithResponses(url)
	if err != nil {
		slog.Error("Failed to create client", "error", err)
		os.Exit(1)
	}

	// Create main context for the application
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	app_, err := app.New(ctx, version, appInfo, httpClient)
	if err != nil {
		panic(err)
	}

	program := tea.NewProgram(
		tui.NewModel(app_),
		tea.WithAltScreen(),
		tea.WithKeyboardEnhancements(),
		tea.WithMouseCellMotion(),
	)

	eventClient, err := client.NewClient(url)
	if err != nil {
		slog.Error("Failed to create event client", "error", err)
		os.Exit(1)
	}

	evts, err := eventClient.Event(ctx)
	if err != nil {
		slog.Error("Failed to subscribe to events", "error", err)
		os.Exit(1)
	}

	go func() {
		for item := range evts {
			program.Send(item)
		}
	}()

	// Run the TUI
	result, err := program.Run()
	if err != nil {
		slog.Error("TUI error", "error", err)
	}

	slog.Info("TUI exited", "result", result)
}
