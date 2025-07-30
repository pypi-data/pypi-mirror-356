import { ICellModel } from '@jupyterlab/cells';
import { JSONValue } from '@lumino/coreutils';

import { IMetadataHandler } from './token';

const TIMEOUT = 500;

interface IDict<T = any> {
  [key: string]: T;
}

/**
 * The metadata updater, which eventually perform changes in metadata.
 */
export class MetadataUpdater {
  /**
   * Handle the change of metadata on a pasted cell.
   *
   * @param model - the cell model.
   * @param handler - the metadata handler.
   */
  handlePastedCell(model: ICellModel, handler?: IMetadataHandler) {
    // If the cell is already handled by new cell handler, skip it.
    this.skipNewCell(model);

    // If an handler is provided, update the metadata.
    if (handler) {
      this._updateMetadata(model, handler);
    }

    // Keep the pasted cell model in memory for a timeout, in case the new cell event
    // is triggered later.
    this._pastedCells.set(
      model,
      setTimeout(this._deletePastedCell, TIMEOUT, model)
    );
  }

  /**
   * Handle the change of metadata on a new cell.
   *
   * @param model - the cell model.
   * @param handler - the metadata handler.
   */
  handleNewCell(model: ICellModel, handler: IMetadataHandler) {
    // If the cell is already handled as a pasted cell, the handler for new cell should
    // not be added.
    if (!this._pastedCells.get(model)) {
      // Defer the change, in case the new cell is a pasted one and the new cell event
      // should be cancelled.
      this._newCells.set(
        model,
        setTimeout(this._updateMetadata, TIMEOUT, model, handler)
      );
    }
  }

  /**
   * Skip a deferred new cell update.
   *
   * @param model - the cell model.
   */
  skipNewCell(model: ICellModel) {
    if (this._newCells.get(model)) {
      clearTimeout(this._newCells.get(model));
      this._newCells.delete(model);
    }
  }

  /**
   * Delete the pasted cell from memory.
   *
   * @param model - the cell model.
   */
  private _deletePastedCell = (model: ICellModel): boolean => {
    return this._pastedCells.delete(model);
  };

  /**
   * Perform the change on the cell metadata.
   *
   * @param model - the cell model.
   * @param handler - the metadata handler.
   */
  private _updateMetadata = (
    model: ICellModel,
    handler: IMetadataHandler
  ): void => {
    // Delete the new cell timeout if exist.
    // no-op if the update comes from a pasted cell.
    this._newCells.delete(model);

    const path = handler.path.split('/');

    const root = path.shift();
    const last = path.pop();

    if (!root) {
      // If root is empty and action is delete, remove the whole metadata.
      if (handler.action === 'delete') {
        const sharedModel = model.sharedModel;
        sharedModel.transact(() =>
          Object.keys(sharedModel.metadata).forEach(key =>
            sharedModel.deleteMetadata(key)
          )
        );
      }
      return;
    }

    const metadata = model.getMetadata(root);

    if (last !== undefined) {
      // There is a nested path.

      // The initial value of the root metadata.
      const obj: IDict<JSONValue> =
        metadata !== undefined ? { ...metadata } : {};

      // The nested item of the metadata.
      let item: IDict<JSONValue> = obj;
      if (path.length) {
        item = path.reduce<IDict<JSONValue>>((acc, key) => {
          if (acc[key]) {
            // If one of the nested subpath was not an object, it will be overwritten.
            if (typeof acc[key] !== 'object') {
              acc[key] = {};
            }
          } else {
            acc[key] = {};
          }
          return acc[key] as IDict<JSONValue>;
        }, obj);
      }
      if (handler.action === 'add') {
        item[last] = handler.value;
      } else if (handler.action === 'delete') {
        delete item[last];
      }
      model.setMetadata(root, obj);
    } else {
      // There is no nested path.
      if (handler.action === 'add') {
        model.setMetadata(root, handler.value);
      } else {
        model.deleteMetadata(root);
      }
    }
  };

  private _pastedCells = new Map<ICellModel, number>();
  private _newCells = new Map<ICellModel, number>();
}
