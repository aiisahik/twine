import { Injectable } from '@angular/core';
import { Http, Response, BaseRequestOptions } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map'

@Injectable()
export class AuthService {
    public token: string;

    constructor(private http: Http) {
        // set token if saved in local storage
        var currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.token = currentUser && currentUser.token;
    }

    login(username: string, password: string): Observable<boolean> {
        let options = new AuthRequestOptions();
        // return this.http.post('/api/v1/token-auth/', JSON.stringify({ username: username, password: password }), options )
        return this.http.post('/api/v1/drf-token-auth/', JSON.stringify({ username: username, password: password }), options )
            .map((response: Response) => {
                // login successful if there's a jwt token in the response
                let token = response.json() && response.json().token;
                if (token) {
                    // set token property
                    this.token = token;

                    // store username and jwt token in local storage to keep user logged in between page refreshes
                    localStorage.setItem('currentUser', JSON.stringify({ username: username, token: token }));

                    // return true to indicate successful login
                    return true;
                } else {
                    // return false to indicate failed login
                    return false;
                }
            })
            .catch(this.handleError);
    }

    handleError(error: Response | any) {
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }

    logout(): void {
        // clear token remove user from local storage to log user out
        this.token = null;
        localStorage.removeItem('currentUser');
    }
}

@Injectable()
export class AuthRequestOptions extends BaseRequestOptions {

  constructor() {
    super();
    // Set the default 'Content-Type' header
    this.headers.set('Content-Type', 'application/json');
    let currentUserStr = localStorage.getItem('currentUser');
    if (typeof currentUserStr === 'string' && currentUserStr.length > 0){
        let currentUser = JSON.parse(currentUserStr);
        if (currentUser && typeof currentUser.token === 'string' && currentUser.token.length > 0){
            console.log('setting auth token in headers', currentUser.token);
            this.headers.set('Authorization', 'Token ' + currentUser.token);
            // this.headers.set('token', currentUser.token);
        }
    }
  }
}