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
        $scope.supplyController = function($scope, $http){
            $scope.victoryCards =[];
            $scope.treasureCards =[];
            $scope.kingdomCards = [];
            $scope.nonSupplyCards =[];
            $scope.miscCards = [];

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
            $scope.updateSupply();


        };

        $scope.handController = function($scope, $http) {
            $scope.hand = [{"name":"chapel","cost":2,"desc":"","type":"ActionCard","src":"/static/images/chapel.png"}];
            $scope.actions = 1;
            $scope.buys = 1;
            
            

            $scope.updateHand = function(){
                $http.get('/hand/'+window.gameid).success(
                    function(data) {
                    $scope.hand = data;
                });
            };
            $scope.updateHand();

            $scope.playCard = function(card) {
                if ($scope.actions == 0){
                    return
                }
                $http.post('/play/'+card+'/'+window.gameid).success(
                    function(data) {
                        $scope.hand = data;
                    });
                $scope.updateHand();
            };

            $scope.discardCard = function() {
                $http.post('discard/'+card+'/'+window.gameid).success(
                    function(data) {
                        $scope.hand = data;
                    });
            };
        };

})(window);