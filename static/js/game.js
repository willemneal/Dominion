(function(window) {
    var dominion = angular.module('dominion', []);
    dominion.directive('shortcut', function() {
        return {
            restrict: 'E',
            replace: true,
            scope: true,
            link: function postLink(scope, iElement, iAttrs) {
                jQuery(document).on('keypress', function(e) {
                    scope.$apply(scope.keyPressed(e));
                });
            }
        };
    });

    
    

    window.gameid = window.location.href.split('/').splice(-1)[0];
    window.gameController = function($scope, $http){
        $scope.hand = [];
        $scope.phase = '';
        $scope.supply = [];
        $scope.log = [];
        $scope.victoryCards =[];
        $scope.treasureCards =[];
        $scope.kingdomCards = [];
        $scope.nonSupplyCards =[];
        $scope.miscCards = [];
        $scope.hand = [{"name":"chapel",
                        "cost":2,"desc":"",
                        "type":"ActionCard",
                        "src":"/static/images/chapel.png"}];
        $scope.actions = 1;
        $scope.buys = 1;
        $scope.prompt = ''

        var source = new EventSource('/stream');
        source.onmessage = function (event) {
            console.log(event)
            unpackState(JSON.parse(event.data));
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
        

        unpackState = function(state){
                        $scope.hand = state['hand'];
                        $scope.phase = state['phase'];
                        $scope.supply = state['supply'];
                        $scope.log = state['log'];
                        $scope.prompt = state['prompt'];
                     };  
            
            
        $scope.initialState = function(){
            $http.post('/state/'+window.gameid).success(
                    function(data) {
                        unpackState(data);
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

        $scope.updateState = function(){
            $http.get('/update/'+window.gameid)
        }
               
        $scope.playCard = function(card) {
            if (card.type == "ActionCard"){
                if ($scope.actions == 0){
                    return
                }
            }
            if (card.type == "TreasureCard"){
                if ($scope.actionPhase()){
                    return
                }
            }
            $http.post('/play/'+card+'/'+window.gameid).success(
                function(data) {
                    $scope.hand = data;
                    $scope.updateState();
                });;
        };

        $scope.discardCard = function() {
            $http.post('discard/'+card+'/'+window.gameid).success(
                function(data) {
                    $scope.hand = data;
                });
        };

        $scope.updateSupply();
        $scope.initialState();
        $scope.updateHand();
    };
})(window);