'use strict'
import * as waapi from 'waapi-client';
import { ak } from 'waapi';

function createObject(client, parent_path_id, object_type, object_name) {
    var args = {
        "parent": parent_path_id,
        "type": object_type,
        "name": object_name
    }
    client.call(ak.wwise.core.object.create, args);
}


async function main() {

    try {
        // Connect to WAAPI
        // Ensure you enabled WAAPI in Wwise's User Preferences
        var client = await waapi.connect('ws://localhost:8080/waapi');

        // Obtain information about Wwise
        var wwiseInfo = await client.call(ak.wwise.core.getInfo, {});
        console.log(`Hello ${wwiseInfo.displayName} ${wwiseInfo.version.displayName}!`);


        // Create a new Wwise Sound object in the default work unit
        createObject(client, "\\Actor-Mixer Hierarchy\\Default Work Unit", "Sound", "MySound123")

        // Disconnect everything
        await client.disconnect();
    }
    catch (e) {
        console.log(e);
    }

    process.exit();
}

main();