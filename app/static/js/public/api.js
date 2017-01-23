'use strict';

angular.module('butternut.public.api', [])
    .factory('loginAPI', ['$resource', function ($resource) {
        return $resource('/api/v1/user/login/', {},
            {
                query: {isArray: false, method: 'POST' },
            }
        );
    }])
;