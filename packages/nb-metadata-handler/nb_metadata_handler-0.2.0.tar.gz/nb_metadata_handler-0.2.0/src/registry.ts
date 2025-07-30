import {
  IMetadataHandler,
  IMetadataHandlerRegistry,
  InsertMethod
} from './token';

/**
 * The default implementation of the metadata handler registry.
 */
export class MetadataHandlerRegistry implements IMetadataHandlerRegistry {
  /**
   * Add a new metadata handler.
   * No-op if the same is already registered.
   */
  add(handler: IMetadataHandler): boolean {
    const index = this._metadataHandlers.findIndex(
      h => h.action === handler.action && h.path === handler.path
    );
    if (index !== -1) {
      return false;
    }
    this._metadataHandlers.push(handler);
    return true;
  }

  /**
   * Remove a metadata handler.
   */
  remove(handler: IMetadataHandler) {
    const index = this._metadataHandlers.findIndex(
      h => h.action === handler.action && h.path === handler.path
    );
    if (index !== -1) {
      this._metadataHandlers.splice(index, 1);
    }
  }

  /**
   * Get the metadata handlers associated to given methods.
   */
  get(methods?: InsertMethod[]): IMetadataHandler[] {
    return this._metadataHandlers.filter(handler =>
      methods?.includes(handler.method)
    );
  }

  private _metadataHandlers: IMetadataHandler[] = [];
}
