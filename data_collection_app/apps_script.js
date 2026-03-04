/**
 * GOOGLE APPS SCRIPT - COLLECTE AUDIO BEJAIA
 * Ce script reçoit les fichiers audio et les classe automatiquement
 * par Contributeur et par Scénario dans votre Google Drive.
 *
 * INSTRUCTIONS D'INSTALLATION :
 * 1. Allez sur https://script.google.com/
 * 2. Créez un "Nouveau Projet"
 * 3. Effacez le code existant et collez tout ce fichier.
 * 4. Cliquez sur "Déployer" > "Nouveau déploiement"
 * 5. Type : "Application Web"
 * 6. Exécuter en tant que : "Moi"
 * 7. Qui a accès : "Tout le monde"
 * 8. Copiez l'URL générée et mettez-la dans la variable UPLOAD_URL de votre index.html
 */

// Nom du dossier principal à la racine de votre Google Drive
const MAIN_FOLDER_NAME = "Donnees_Audio_Bejaia";

function doPost(e) {
  try {
    // 1. Lire les données envoyées par l'application web
    var data = JSON.parse(e.postData.contents);
    var base64Data = data.audio;
    var filename = data.filename || "audio.webm";
    var userFolder = data.userFolder || "Anonyme";
    var scenarioFolder = data.scenarioFolder || "Inconnu";

    // 2. Décoder l'audio
    var decoded = Utilities.base64Decode(base64Data);
    var blob = Utilities.newBlob(decoded, getMimeType(filename), filename);

    // 3. Trouver ou créer l'arborescence des dossiers
    var mainDir = getOrCreateFolder(DriveApp.getRootFolder(), MAIN_FOLDER_NAME);
    var userDir = getOrCreateFolder(mainDir, userFolder);
    var sceneDir = getOrCreateFolder(userDir, scenarioFolder);

    // 4. Sauvegarder le fichier dans le dossier final
    var file = sceneDir.createFile(blob);

    // 5. Renvoyer une réponse de succès
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      url: file.getUrl(),
      path: MAIN_FOLDER_NAME + "/" + userFolder + "/" + scenarioFolder + "/" + filename
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Gestion des erreurs
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * GET endpoint — retourne les statistiques de collecte.
 * Appelé par le frontend pour afficher la progression globale
 * et prioriser les scénarios pas encore couverts.
 *
 * Réponse JSON :
 * {
 *   total_audios: 142,
 *   total_contributors: 5,
 *   scenarios: { "SYN_drowning_001__00030": { contributors: 3, files: 24 }, ... }
 * }
 */
function doGet(e) {
  try {
    var mainDir = getMainFolder();
    if (!mainDir) {
      return jsonResponse({ total_audios: 0, total_contributors: 0, scenarios: {}, users: [] });
    }

    var stats = { total_audios: 0, total_contributors: 0, scenarios: {}, users: [] };

    // Parcourir chaque dossier utilisateur
    var userFolders = mainDir.getFolders();
    while (userFolders.hasNext()) {
      var userDir = userFolders.next();
      stats.total_contributors++;
      stats.users.push(userDir.getName().toLowerCase());

      // Parcourir chaque dossier scénario
      var scenarioFolders = userDir.getFolders();
      while (scenarioFolders.hasNext()) {
        var sceneDir = scenarioFolders.next();
        var sceneName = sceneDir.getName();
        var fileCount = 0;
        var turnCounts = {}; // { "t01_caller": 1, "t02_operator": 1, ... }
        var files = sceneDir.getFiles();
        while (files.hasNext()) {
          var file = files.next();
          fileCount++;
          // Parser le nom pour extraire le turn: ..._t01_caller.webm
          var match = file.getName().match(/_t(\d+)_(caller|operator)\./);
          if (match) {
            var turnKey = "t" + match[1] + "_" + match[2];
            turnCounts[turnKey] = (turnCounts[turnKey] || 0) + 1;
          }
        }
        stats.total_audios += fileCount;
        if (!stats.scenarios[sceneName]) {
          stats.scenarios[sceneName] = { contributors: 0, files: 0, turns: {} };
        }
        stats.scenarios[sceneName].contributors++;
        stats.scenarios[sceneName].files += fileCount;
        // Agréger les turns: compter combien de contributeurs uniques par turn
        for (var tk in turnCounts) {
          stats.scenarios[sceneName].turns[tk] = (stats.scenarios[sceneName].turns[tk] || 0) + 1;
        }
      }
    }

    return jsonResponse(stats);

  } catch (error) {
    return jsonResponse({ error: error.toString() });
  }
}

// Gère les options CORS (Pre-flight requests)
function doOptions(e) {
  return ContentService.createTextOutput("")
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Cherche le dossier principal sans le créer (pour doGet)
 */
function getMainFolder() {
  var folders = DriveApp.getRootFolder().getFoldersByName(MAIN_FOLDER_NAME);
  if (folders.hasNext()) return folders.next();
  return null;
}

/**
 * Fonction utilitaire pour trouver un dossier par son nom ou le créer s'il n'existe pas
 */
function getOrCreateFolder(parentFolder, folderName) {
  // Nettoyer le nom du dossier pour éviter les caractères invalides
  var safeFolderName = folderName.replace(/[^a-zA-Z0-9_\-\s]/g, "").trim();

  var folders = parentFolder.getFoldersByName(safeFolderName);
  if (folders.hasNext()) {
    return folders.next(); // Le dossier existe, on le retourne
  } else {
    return parentFolder.createFolder(safeFolderName); // Le dossier n'existe pas, on le crée
  }
}

/**
 * Déduit le type MIME selon l'extension pour que Google Drive le reconnaisse bien
 */
function getMimeType(filename) {
  if (filename.indexOf('.webm') > -1) return 'audio/webm';
  if (filename.indexOf('.m4a') > -1 || filename.indexOf('.mp4') > -1) return 'audio/mp4';
  if (filename.indexOf('.aac') > -1) return 'audio/aac';
  if (filename.indexOf('.ogg') > -1) return 'audio/ogg';
  if (filename.indexOf('.mp3') > -1) return 'audio/mpeg';
  return 'application/octet-stream';
}

/**
 * Helper pour retourner du JSON proprement
 */
function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
