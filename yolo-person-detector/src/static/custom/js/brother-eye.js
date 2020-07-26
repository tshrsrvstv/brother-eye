(function(){
    'use strict';

    const brotherEyeApp = angular.module('BrotherEyeApp',[]);
    brotherEyeApp.controller('BrotherEyeController', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
        //x-axis markings
        $scope.labels = [];
        //data-store
        $scope.data = [
            []
        ];
        $scope.options = {
            animation: {
                duration: 0
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Person Count'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }]
            }
        };
        var ctx = document.getElementById("chart").getContext('2d');
        //Initializing Chart for Persons detected in frame
        var personChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Persons in Frame',
                    data: $scope.data[0],
                    backgroundColor: "rgba(155, 216, 245, 0.3)",
                    borderColor: "#316fdf"
                }],
                labels: $scope.labels
            },
            options: $scope.options
        });
        //Polling backend service for getting detected persons count.
        $interval(function(){
            $http.get('/persons')
                .success(function(response){
                    $scope.labels.push(response.time);
                    $scope.data[0].push(response.count);
                    if($scope.data[0].length>60){
                        $scope.data[0].splice(0,1);
                        $scope.labels.splice(0,1);
                    }
                    personChart.update({duration: 0});
                });
        }, 1000);

    }]);
}());