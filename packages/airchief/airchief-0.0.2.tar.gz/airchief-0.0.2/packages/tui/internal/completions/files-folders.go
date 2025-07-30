package completions

import (
	"context"

	"github.com/shaneholloman/airchief/internal/app"
	"github.com/shaneholloman/airchief/internal/components/dialog"
	"github.com/shaneholloman/airchief/pkg/client"
)

type filesAndFoldersContextGroup struct {
	app    *app.App
	prefix string
}

func (cg *filesAndFoldersContextGroup) GetId() string {
	return cg.prefix
}

func (cg *filesAndFoldersContextGroup) GetEntry() dialog.CompletionItemI {
	return dialog.NewCompletionItem(dialog.CompletionItem{
		Title: "Files & Folders",
		Value: "files",
	})
}

func (cg *filesAndFoldersContextGroup) GetEmptyMessage() string {
	return "no matching files"
}

func (cg *filesAndFoldersContextGroup) getFiles(query string) ([]string, error) {
	response, err := cg.app.Client.PostFileSearchWithResponse(context.Background(), client.PostFileSearchJSONRequestBody{
		Query: query,
	})
	if err != nil {
		return []string{}, err
	}
	if response.JSON200 == nil {
		return []string{}, nil
	}

	return *response.JSON200, nil
}

func (cg *filesAndFoldersContextGroup) GetChildEntries(query string) ([]dialog.CompletionItemI, error) {
	matches, err := cg.getFiles(query)
	if err != nil {
		return nil, err
	}

	items := make([]dialog.CompletionItemI, 0, len(matches))
	for _, file := range matches {
		item := dialog.NewCompletionItem(dialog.CompletionItem{
			Title: file,
			Value: file,
		})
		items = append(items, item)
	}

	return items, nil
}

func NewFileAndFolderContextGroup(app *app.App) dialog.CompletionProvider {
	return &filesAndFoldersContextGroup{
		app:    app,
		prefix: "file",
	}
}
