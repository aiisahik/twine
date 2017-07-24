import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map'

// import { AuthService } from '../_services/auth.service';
import { Profile } from '../_models/profile';

@Injectable()
export class ProfileService {
    constructor(
        private http: Http,
        // private authenticationService: AuthService
    ) {
    }

    getProfile(): Observable<Profile[]> {
        // add authorization header with jwt token
        // let headers = new Headers({ 'Authorization': 'Bearer ' + this.authenticationService.token });
        // let options = new RequestOptions({ headers: headers });
        let options = new RequestOptions({  });

        // get users from api
        return this.http.get('/api/v1/account/profile', options)
            .map((response: Response) => response.json());
    }
}