

    window.gameid = window.location.href.split('/').splice(-1)[0];
    console.log(document.location);
    angular.module('Dominion', []).controller('GameController',["$scope","$http",

    function  ($scope, $http){
        $scope.hand = [];
        $scope.phase = '';
        $scope.supply = [];
        $scope.log = [];
        $scope.victoryCards =[];
        $scope.treasureCards =[];
        $scope.kingdomCards = [];
        $scope.nonSupplyCards =[];
        $scope.miscCards = [];
        $scope.hand = [];
        $scope.actions = 1;
        $scope.buys = 1;
        $scope.coins = 0;
        $scope.prompt = '';
        $scope.choice = null;
        $scope.categories = ["victoryCards", "treasureCards", "kingdomCards", "miscCards", "nonSupplyCards"];

        //This is for connecting to the event stream which pushes updates


        $scope.gainCard = function(card){
            if ($scope.choice == null){
                return;
            }
            if ($scope.choice['type'] != 'gain'){
                return;
            }

            if ($scope.phase == "buy" & $scope.choice['type'] != "gain"){
                if (card.cost > $scope.coins | card in $scope.supply['nonSupplyCards']){
                    return;
                }
                $http.post('/buy/'+card.name + "/" + window.gameid).success(
                    function(data){
                        $scope.updateState();
                    }
                    );
            }

        };

        $scope.endTurn = function(){
            $http.post('/endTurn/'+window.gameid).success(
                function(data){
                    $scope.updateState();
                });
        };

        $scope.actionPhase = function(){
            return $scope.phase == 'action'
        };
        $scope.buyPhase = function(){
            return $scope.phase == 'buy'
        };
        $scope.waiting =function(){
            return $scope.phase = 'waiting'
        };

        $scope.chooseOption = function(option){
            $http.post("/choice/"+option+"/"+window.gameid).success(
                function(data){
                    updateState();
                });
        };


        unpackState = function(state){
                        if (state==1){
                            $scope.updateState();
                            return
                        }
                        console.log(state);
                        $scope.state = state;
                        $scope.hand = state['hand'];
                        $scope.phase = state['phase'];
                        $scope.supply = state['supply'];
                        $scope.victoryCards   = $scope.supply["victoryCards"]
                        $scope.treasureCards  = $scope.supply["treasureCards"];
                        $scope.kingdomCards   = $scope.supply["kingdomCards"];
                        $scope.nonSupplyCards = $scope.supply["nonSupplyCards"];
                        $scope.miscCards      = $scope.supply["miscCards"];

                        $scope.log = state['log'];

                        if ($scope.phase == "waiting"){
                            $scope.actions = 1;
                            $scope.buys    = 1;
                            $scope.coins   = 0;
                        }
                        else{
                            $scope.actions = $scope.state['turn']['actions'];
                            if ($scope.phase == "action" & $scope.actions == 0){
                                $scope.startBuyPhase();
                            }

                            $scope.buys    = $scope.state['turn']['buys'];
                            if ($scope.phase == "buy" & $scope.buys == 0){
                                $scope.endTurn();
                            }

                            $scope.coins   = state['turn']['coins'];
                        }
                        $scope.categories = state['supply']['categories'];
                        console.log(state['supply']['categories']);
                        $scope.choice = null;
                        $scope.prompt = '';
                        if (state['choice']){
                            $scope.choice = state['choice'];
                            $scope.prompt = state['choice']['prompt'];
                        }
                     };

        $scope.isOptions = function(){
            if ($scope.choice == null){
                return false
            }
            return $scope.choice['type'] == "options";
        };

        $scope.skipChoice = function(){
            $http.post('/skip/'+window.gameid).success(
                function(data){ $scope.updateState()});

        }

        $scope.initialState = function(){
            $http.post('/state/'+window.gameid).success(
                    function(data) {
                        $scope.$apply(unpackState(data));
                });
        };

        $scope.updateSupply = function(){
            $http.get('/supply/'+window.gameid).success(
                function(data) {
                    $scope.victoryCards   = data["victoryCards"]
                    $scope.treasureCards  = data["treasureCards"];
                    $scope.kingdomCards   = data["kingdomCards"];
                    $scope.nonSupplyCards = data["nonSupplyCards"];
                    $scope.miscCards      = data["miscCards"];
            });
        };
        $scope.updateHand = function(){
            $http.get('/hand/'+window.gameid).success(
                function(data) {
                    $scope.hand = data;
            });
        };



        $scope.playAllTreasures  = function(){
            for (var i=0; i<$scope.hand.length; i++){
                if ($scope.hand[i]['type'] == "TreasureCard"){
                    $scope.playCard($scope.hand[i]);
                }
            }
        }

        $scope.playCard = function(card) {
            console.log(card.name + " clicked");

            if ($scope.choice==null | $scope.choice['type'] != 'fromHand'){
                return;
            }
            if (card.type == "ActionCard"){
                if ($scope.actions == 0 | $scope.buyPhase()|
                    $scope.choice['kind']== "TreasureCard"){
                    return;
                }
            }
            if (card.type == "TreasureCard"){
                if ($scope.choice['kind'] == "ActionCard"){
                    return;
                }
            }
            $http.post(encodeURI('/play/'+card.name +'/' + window.gameid + "?callback=" +$scope.choice['callback'])).success(
                function(data){
                    $scope.updateState();
                });
        };

        $scope.startBuyPhase = function(){
            $http.post('/buyPhase/'+window.gameid).success(
                function(data){
                    $scope.updateState();
            });

        };

        $scope.discardCard = function() {
            $http.post('discard/'+card+'/'+window.gameid).success(
                function(data) {
                    $scope.hand = data;
                });
        };
        var socketLocation = window.location.origin+":"+window.location.port+'/update';
        socket = io.connect(socketLocation);
        $scope.updateState = function(){
            //$http.get('/update/'+window.gameid);
            socket.emit('Game Event',{'room':window.gameid});
            console.log("Asking for new state for everyone");
        }



        console.log(socketLocation);


        socket.on('getState', function(msg) {
            console.log("asking for my state");
            socket.emit('getUpdate',{'room':window.gameid});
        });

        socket.on('state', function(msg) {
            $scope.$apply(unpackState(msg['state']));
            console.log(msg);
        });


        socket.on('message', function(msg){
                console.log(msg.data);
        });


        socket.emit("join",{'room':window.gameid});

        $scope.updateState();

    }
]);
