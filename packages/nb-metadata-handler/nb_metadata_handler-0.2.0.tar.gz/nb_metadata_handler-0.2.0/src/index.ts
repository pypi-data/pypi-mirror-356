import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICellModel } from '@jupyterlab/cells';
import { CellList, INotebookTracker, Notebook } from '@jupyterlab/notebook';
import { IObservableList } from '@jupyterlab/observables';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import {
  ReadonlyPartialJSONArray,
  ReadonlyPartialJSONObject
} from '@lumino/coreutils';

import { MetadataUpdater } from './metadata-updater';
import { MetadataHandlerRegistry } from './registry';
import {
  IMetadataHandler,
  IMetadataHandlerRegistry,
  InsertMethod
} from './token';

/**
 * The plugin that will track the cell insertion in all notebooks, and call the
 * metadata updater with the relevant changes.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'nb-metadata-handler:plugin',
  description: 'A JupyterLab extension to handle notebook metadata.',
  autoStart: true,
  requires: [IMetadataHandlerRegistry, INotebookTracker],
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    registry: IMetadataHandlerRegistry,
    tracker: INotebookTracker,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('JupyterLab extension nb-metadata-handler is activated!');
    const notebookReady = new Map<Notebook, boolean>();

    const updater = new MetadataUpdater();

    const cellPasted = (
      notebook: Notebook,
      pasteCells: Notebook.IPastedCells
    ) => {
      let handlers: IMetadataHandler[] = [];
      if (
        pasteCells.previousInteraction === 'copy' ||
        pasteCells.previousInteraction === 'paste'
      ) {
        handlers = registry.get(['all', 'copyPaste']);
      } else if (pasteCells.previousInteraction === 'cut') {
        handlers = registry.get(['all', 'cutPaste']);
      }

      const cellModels: ICellModel[] = [];
      for (let i = pasteCells.cellCount - 1; i >= 0; i--) {
        const index = notebook.activeCellIndex - i;
        cellModels.push(notebook.widgets[index].model);
      }

      cellModels.forEach(model => {
        updater.skipNewCell(model);
        if (handlers.length) {
          handlers.forEach(handler => updater.handlePastedCell(model, handler));
        } else {
          updater.handlePastedCell(model);
        }
      });
    };

    const cellsChanged = (
      cells: CellList,
      change: IObservableList.IChangedArgs<ICellModel>
    ) => {
      if (change.type !== 'add') {
        return;
      }
      const handlers: IMetadataHandler[] = registry.get(['all', 'new']);
      change.newValues.forEach(model => {
        handlers.forEach(handler => updater.handleNewCell(model, handler));
      });
    };

    tracker.widgetAdded.connect((sender, notebookPanel) => {
      const notebook = notebookPanel.content;
      notebookReady.set(notebook, false);
      notebook.model?.stateChanged.connect((model, change) => {
        if (notebookReady.get(notebook)) {
          return;
        }
        if (change.name === 'dirty' && change.newValue === false) {
          notebookReady.set(notebook, true);
          notebook.cellsPasted.connect(cellPasted);
          notebook.model?.cells.changed.connect(cellsChanged);
          notebook.disposed.connect(() => {
            notebook.cellsPasted.disconnect(cellPasted);
            notebook.model?.cells.changed.disconnect(cellsChanged);
            notebookReady.delete(notebook);
          });
        }
      });
    });

    /**
     * Handle the settings.
     */
    let registeredHandlers: IMetadataHandler[] = [];
    const loadSetting = (setting: ISettingRegistry.ISettings): void => {
      // Get the handlers from settings
      const handlers = setting.get('handlers')
        .composite as ReadonlyPartialJSONArray;

      // Remove previous handlers added by the settings
      registeredHandlers.forEach(handler => registry.remove(handler));
      registeredHandlers = [];

      handlers.forEach(handlerSetting => {
        if (!handlerSetting) {
          return;
        }
        handlerSetting = handlerSetting as ReadonlyPartialJSONObject;
        let handler: IMetadataHandler | undefined;

        if (handlerSetting['action'] === 'delete') {
          // Create an handler to delete metadata
          handler = {
            action: 'delete',
            method: handlerSetting['method'] as InsertMethod,
            path: handlerSetting['path'] as string
          };
        } else if (handlerSetting['action'] === 'add') {
          /**
           * Create an handler to add metadata
           * We first try to parse the value. It should work if the value type is of
           * - number
           * - boolean
           * - object
           * - array
           * If an error is caught, this means that the value is a string.
           */
          let value: any;
          try {
            value = JSON.parse(handlerSetting['value'] as string);
          } catch {
            value = handlerSetting['value'] as string;
          }

          handler = {
            action: 'add',
            method: handlerSetting['method'] as InsertMethod,
            path: handlerSetting['path'] as string,
            value: value
          };
        }
        if (!handler) {
          return;
        }

        // Add the handler to the register
        if (registry.add(handler)) {
          registeredHandlers.push(handler);
        }
      });
    };

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          loadSetting(settings);
          settings.changed.connect(loadSetting);
        })
        .catch(reason => {
          console.error(
            'Failed to load settings for nb-metadata-handler.',
            reason
          );
        });
    }
  }
};

/**
 * The metadata handler registry.
 */
const registry: JupyterFrontEndPlugin<IMetadataHandlerRegistry> = {
  id: 'nb-metadata-handler:registry',
  description: 'A registry of metadata handler.',
  autoStart: true,
  provides: IMetadataHandlerRegistry,
  activate: (app: JupyterFrontEnd): IMetadataHandlerRegistry => {
    return new MetadataHandlerRegistry();
  }
};

export default [plugin, registry];
export * from './token';
