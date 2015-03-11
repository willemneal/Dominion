    getGameID = function (){
        var gameid = window.location.href.split('/').splice(-1)[0];
        if (gameid.indexOf("?") != -1){
            gameid = gameid.substring(0,gameid.indexOf("?"));
        }
        return gameid
    }

    window.gameid = getGameID();//Global variable

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
        $scope.categories = [];

        //This is for connecting to the event stream which pushes updates


        $scope.chooseCard = function(card){
            if ($scope.choice == null){
                return;
            }
            if ($scope.buyPhase()){
              $scope.choice['type'] = 'buy';
            }
            switch ($scope.choice['type']){
                case 'gain':
                    gainCard(card);
                    console.log(card.name + " gained");
                    break;
                case 'buy':
                    if (!$scope.buyPhase()){
                        console.log('Not the buyPhase');
                        return;
                    }
                    buyCard(card);
                    console.log(card.name + " Bought");
                    break;
                default:
                    console.log("nothing to do... Not right");
                    break;
            }

        };
        buyCard = function(card){
            if (card.cost > $scope.coins | card in $scope.supply['nonSupplyCards']
                | pileEmpty(card)){
                return;
            }
            console.log('in Buycard');
            $http.post('/buy/'+card.name + "/" + window.gameid).success(
                function(data){
                    $scope.updateState();
                }
                );
        };

        gainCard = function(card){
            if (pileEmpty(card) | ($scope.choice.kind && $scope.choice.kind != card.kind))
                return;
            if (( $scope.choice.exact &&  $scope.choice.cost != card.cost)||
                $scope.choice.cost > card.cost)
                return;
            $http.post('/gain/'+card.name + "/" + window.gameid).success(
                function(data){
                    $scope.updateState();
                }
                );
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

        pileEmpty = function(card){
            return $scope.supply[card.name].numberLeft == 0;
        };

        $scope.skipChoice = function(){
            $http.post('/skip/'+window.gameid).success(
                function(data){ $scope.updateState()});

        };

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
            socket.emit("PlayAllTreasures",{"time": new Date().toDateString()});
        }

        correctKind = function(card){
            if ($scope.choice['kind']==card.type){
                return card.kind != $scope.choice.kind;
            }
            return true;
        };

        $scope.playCard = function(card) {
            console.log(card.name + " clicked");

            /*
            Return if:
            -no choice
            -not choice from hand
            -if the there is a kind choice card is right kind
            */
            if ($scope.choice==null | $scope.choice['type'] != 'fromHand'
                | !correctKind(card)){
                return;
            }
            // if ($scope.buyPhase()){
            //     if (card.type == "ActionCard"){
            //         return;
            //     }
            // }
            // if (card.type == "ActionCard"  && ($scope.actions == 0 || $scope.buyPhase()||
            //     $scope.choice['kind']== "TreasureCard")){
            //         return;
            //
            // }
            // if (card.type == "TreasureCard"  && $scope.choice['kind'] == "ActionCard"){
            //     return;
            // }
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
