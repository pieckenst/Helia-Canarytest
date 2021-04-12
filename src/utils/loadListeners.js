const path = require('path');
const fs = require('fs').promises;
const Listener = require('../structures/Listener');

module.exports = async function loadListeners(client, dir, reset = false) {
    if (reset) {
        client.listeners.clear();
        client.removeAllListeners();
    }
    // fetching all the files in a directory (wholesome 100 reddit big chungus)
    const filesPath = path.join(__dirname, dir);
    const files = await fs.readdir(filesPath);

    for (const file of files) {
        const filePath = path.join(filesPath, file);
        const lstat = await fs.lstat(filePath);

        // recursive listeners loading
        if (lstat.isDirectory())
            await loadListeners(client, path.join(dir, file));
        if (file.endsWith('.js')) {
            let listenerPrototype = require(filePath);

            // if the listener is instance of Listener structure
            // we add this into the listeners collection and
            // start listening
            if (listenerPrototype.prototype instanceof Listener) {
                const listener = new listenerPrototype();
                client.listeners.set(listener.name, listener);
                client.on(
                    listener.emitter,
                    await listener.run.bind(listener, client)
                );
            }
        }
    }
};
