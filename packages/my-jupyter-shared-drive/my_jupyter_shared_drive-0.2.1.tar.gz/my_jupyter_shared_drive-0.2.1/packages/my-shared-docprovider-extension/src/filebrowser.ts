/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

import {
  IEditorWidgetFactory,
  FileEditorFactory
} from '@jupyterlab/fileeditor';
import {
  INotebookWidgetFactory,
  NotebookWidgetFactory
} from '@jupyterlab/notebook';
import { ContentsManager } from '@jupyterlab/services';
import { RtcContentProvider } from '@jupyter/my-shared-docprovider';
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';

import { YFile, YNotebook } from '@jupyter/ydoc';

import { ICollaborativeContentProvider } from '@jupyter/collaborative-drive';

/**
 * The shared drive provider.
 */
export const rtcContentProvider: JupyterFrontEndPlugin<ICollaborativeContentProvider> =
  {
    id: '@jupyter/docprovider-extension:content-provider',
    description: 'The RTC content provider',
    provides: ICollaborativeContentProvider,
    optional: [ITranslator],
    activate: (
      app: JupyterFrontEnd,
      translator: ITranslator | null
    ): ICollaborativeContentProvider => {
      translator = translator ?? nullTranslator;
      const trans = translator.load('my-jupyter-shared-drive');
      const defaultDrive = (app.serviceManager.contents as ContentsManager)
        .defaultDrive;
      if (!defaultDrive) {
        throw Error(
          'Cannot initialize content provider: default drive property not accessible on contents manager instance.'
        );
      }
      const registry = defaultDrive.contentProviderRegistry;
      if (!registry) {
        throw Error(
          'Cannot initialize content provider: no content provider registry.'
        );
      }
      const rtcContentProvider = new RtcContentProvider(app, {
        apiEndpoint: '/api/contents',
        serverSettings: defaultDrive.serverSettings,
        user: app.serviceManager.user,
        trans
      });
      registry.register('rtc', rtcContentProvider);
      return rtcContentProvider;
    }
  };

/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export const yfile: JupyterFrontEndPlugin<void> = {
  id: '@jupyter/my-shared-docprovider-extension:yfile',
  description:
    "Plugin to register the shared model factory for the content type 'file'",
  autoStart: true,
  requires: [ICollaborativeContentProvider, IEditorWidgetFactory],
  optional: [],
  activate: (
    app: JupyterFrontEnd,
    contentProvider: ICollaborativeContentProvider,
    editorFactory: FileEditorFactory.IFactory
  ): void => {
    const yFileFactory = () => {
      return new YFile();
    };
    contentProvider.sharedModelFactory.registerDocumentFactory(
      'file',
      yFileFactory
    );
    editorFactory.contentProviderId = 'rtc';
  }
};

/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export const ynotebook: JupyterFrontEndPlugin<void> = {
  id: '@jupyter/my-shared-docprovider-extension:ynotebook',
  description:
    "Plugin to register the shared model factory for the content type 'notebook'",
  autoStart: true,
  requires: [ICollaborativeContentProvider, INotebookWidgetFactory],
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    contentProvider: ICollaborativeContentProvider,
    notebookFactory: NotebookWidgetFactory.IFactory,
    settingRegistry: ISettingRegistry | null
  ): void => {
    let disableDocumentWideUndoRedo = true;

    // Fetch settings if possible.
    if (settingRegistry) {
      settingRegistry
        .load('@jupyterlab/notebook-extension:tracker')
        .then(settings => {
          const updateSettings = (settings: ISettingRegistry.ISettings) => {
            const enableDocWideUndo = settings?.get(
              'experimentalEnableDocumentWideUndoRedo'
            ).composite as boolean;

            disableDocumentWideUndoRedo = !enableDocWideUndo ?? true;
          };

          updateSettings(settings);
          settings.changed.connect((settings: ISettingRegistry.ISettings) =>
            updateSettings(settings)
          );
        });
    }

    const yNotebookFactory = () => {
      return new YNotebook({
        disableDocumentWideUndoRedo
      });
    };
    contentProvider.sharedModelFactory.registerDocumentFactory(
      'notebook',
      yNotebookFactory
    );
    notebookFactory.contentProviderId = 'rtc';
  }
};
