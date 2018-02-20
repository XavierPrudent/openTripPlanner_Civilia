(function(window, undefined) {
  var dictionary = {
    "7ed5a823-6d29-4330-8976-6b054534f008": "Portal",
    "f16ac9c6-d0be-4c79-bb18-311004bbf7fd": "Ana_stats",
    "359e20c3-cb1b-45fe-897f-a1e7f529c4bd": "Stats",
    "9e4edbeb-874e-4b67-8e87-60e53eedd58d": "OTP",
    "7baad05f-402c-42b3-b156-03ba31d66b8e": "Historique",
    "d12245cc-1680-458d-89dd-4f0d7fb22724": "Accueil",
    "e73b655d-d3ec-4dcc-a55c-6e0293422bde": "960 grid - 16 columns",
    "ef07b413-721c-418e-81b1-33a7ed533245": "960 grid - 12 columns",
    "f39803f7-df02-4169-93eb-7547fb8c961a": "Template 1",
    "bb8abf58-f55e-472d-af05-a7d1bb0cc014": "default"
  };

  var uriRE = /^(\/#)?(screens|templates|masters|scenarios)\/(.*)(\.html)?/;
  window.lookUpURL = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, url;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      url = folder + "/" + canvas;
    }
    return url;
  };

  window.lookUpName = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, canvasName;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      canvasName = dictionary[canvas];
    }
    return canvasName;
  };
})(window);