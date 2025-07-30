import { JSONValue, Token } from '@lumino/coreutils';

/**
 * The insert method types.
 * - new: new cell in this Notebook (can be pasted from another notebook)
 * - copyPaste: cell copy/pasted from the same Notebook
 * - cutPaste: cell cut/pasted from the same Notebook
 * - all: any kind of new cell
 */
export type InsertMethod = 'new' | 'copyPaste' | 'cutPaste' | 'all';

/**
 * The interface of an handler to remove a metadata.
 */
export interface IMetadataRemover {
  /**
   * The action of the metadata handler.
   */
  action: 'delete';
  /**
   * The insert method that should trigger this handler.
   */
  method: InsertMethod;
  /**
   * The path of the metadata.
   */
  path: string;
}

/**
 * The interface of an handler to add a metadata.
 */
export interface IMetadataWriter {
  /**
   * The action of the metadata handler.
   */
  action: 'add';
  /**
   * The insert method that should trigger this handler.
   */
  method: InsertMethod;
  /**
   * The path of the metadata.
   */
  path: string;
  /**
   * The value of the metadata.
   */
  value: JSONValue;
}

/**
 * The metadata handler type.
 */
export type IMetadataHandler = IMetadataRemover | IMetadataWriter;

/**
 * The metadata handler registry interface.
 */
export interface IMetadataHandlerRegistry {
  /**
   * Add a new metadata handler.
   * No-op if the same is already registered.
   */
  add(handler: IMetadataHandler): boolean;
  /**
   * Remove a metadata handler.
   */
  remove(handler: IMetadataHandler): void;
  /**
   * Get the metadata handlers associated to given methods.
   */
  get(methods?: InsertMethod[]): IMetadataHandler[];
}

/**
 * The token exposing the metadata handler registry.
 */
export const IMetadataHandlerRegistry = new Token<IMetadataHandlerRegistry>(
  'nb-metadata-handler:registry',
  'Registry of metadata handlers'
);
