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

        window.handController = function($scope, $http) {
            $scope.hand = [];
            $scope.actions = 1;
            $scope.buys = 1;
            window.gameid = window.location.href.split('/').splice(-1)[0];
            $scope.updateHand();

            $scope.updateHand = function(){
                $http.get('hand/'+window.gameid).success(
                    function(data) {
                    $scope.hand = data;
                });
            };
            $scope.playCard = function(card) {
                $http.post('play/'+card+'/'+window.gameid).success(
                    function(data) {
                        $scope.hand = data;
                    });
            };

            $scope.discardCard = function() {
                $http.post('discard/'+card+'/'+window.gameid).success(
                    function(data) {
                        $scope.hand = data;
                    });
            };
        };

})(window);