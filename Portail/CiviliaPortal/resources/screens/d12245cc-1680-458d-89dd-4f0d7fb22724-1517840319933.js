jQuery("#simulation")
  .on("click", ".s-d12245cc-1680-458d-89dd-4f0d7fb22724 .click", function(event, data) {
    var jEvent, jFirer, cases;
    if(data === undefined) { data = event; }
    jEvent = jimEvent(event);
    jFirer = jEvent.getEventFirer();
    if(jFirer.is("#s-Button_1")) {
      cases = [
        {
          "blocks": [
            {
              "condition": {
                "action": "jimAnd",
                "parameter": [ {
                  "action": "jimGreaterOrEquals",
                  "parameter": [ {
                    "action": "jimCount",
                    "parameter": [ {
                      "datatype": "property",
                      "target": "#s-Input_2",
                      "property": "jimGetValue"
                    } ]
                  },"1" ]
                },{
                  "action": "jimGreaterOrEquals",
                  "parameter": [ {
                    "action": "jimCount",
                    "parameter": [ {
                      "datatype": "property",
                      "target": "#s-Input_1",
                      "property": "jimGetValue"
                    } ]
                  },"1" ]
                } ]
              },
              "actions": [
                {
                  "action": "jimNavigation",
                  "parameter": {
                    "target": "screens/7ed5a823-6d29-4330-8976-6b054534f008"
                  },
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            },
            {
              "actions": [
                {
                  "action": "jimShow",
                  "parameter": {
                    "target": [ "#s-Rectangle_2" ]
                  },
                  "exectype": "serial",
                  "delay": 0
                }
              ]
            }
          ],
          "exectype": "serial",
          "delay": 0
        }
      ];
      event.data = data;
      jEvent.launchCases(cases);
    }
  });