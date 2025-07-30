import { ICollaborativeDrive } from '@jupyter/collaborative-drive';
import { IJCadWorkerRegistryToken, IJupyterCadDocTracker, IJCadExternalCommandRegistryToken } from '@jupytercad/schema';
import { IThemeManager } from '@jupyterlab/apputils';
import { JupyterCadStlModelFactory } from './modelfactory';
import { JupyterCadDocumentWidgetFactory } from '../factory';
import { JupyterCadStlDoc } from './model';
import { stlIcon } from '@jupytercad/base';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
const FACTORY = 'JupyterCAD STL Viewer';
const SETTINGS_ID = '@jupytercad/jupytercad-core:jupytercad-settings';
const activate = async (app, tracker, themeManager, workerRegistry, externalCommandRegistry, drive, settingRegistry) => {
    let settings = null;
    if (settingRegistry) {
        try {
            settings = await settingRegistry.load(SETTINGS_ID);
            console.log(`Loaded settings for ${SETTINGS_ID}`, settings);
        }
        catch (error) {
            console.warn(`Failed to load settings for ${SETTINGS_ID}`, error);
        }
    }
    else {
        console.warn('No settingRegistry available; using default settings.');
    }
    const widgetFactory = new JupyterCadDocumentWidgetFactory({
        name: FACTORY,
        modelName: 'jupytercad-stlmodel',
        fileTypes: ['stl'],
        defaultFor: ['stl'],
        tracker,
        commands: app.commands,
        workerRegistry,
        externalCommandRegistry
    });
    app.docRegistry.addWidgetFactory(widgetFactory);
    const modelFactory = new JupyterCadStlModelFactory(settingRegistry ? { settingRegistry } : {});
    app.docRegistry.addModelFactory(modelFactory);
    app.docRegistry.addFileType({
        name: 'stl',
        displayName: 'STL',
        mimeTypes: ['text/plain'],
        extensions: ['.stl', '.STL'],
        fileFormat: 'text',
        contentType: 'stl',
        icon: stlIcon
    });
    const stlSharedModelFactory = () => {
        return new JupyterCadStlDoc();
    };
    if (drive) {
        drive.sharedModelFactory.registerDocumentFactory('stl', stlSharedModelFactory);
    }
    widgetFactory.widgetCreated.connect((sender, widget) => {
        widget.title.icon = stlIcon;
        widget.context.pathChanged.connect(() => {
            tracker.save(widget);
        });
        themeManager.themeChanged.connect((_, changes) => widget.model.themeChanged.emit(changes));
        tracker.add(widget);
        app.shell.activateById('jupytercad::leftControlPanel');
        app.shell.activateById('jupytercad::rightControlPanel');
    });
};
const stlPlugin = {
    id: 'jupytercad:stlplugin',
    requires: [
        IJupyterCadDocTracker,
        IThemeManager,
        IJCadWorkerRegistryToken,
        IJCadExternalCommandRegistryToken
    ],
    optional: [ICollaborativeDrive, ISettingRegistry],
    autoStart: true,
    activate
};
export default stlPlugin;
