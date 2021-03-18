import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap, finalize } from 'rxjs/operators';
import { TokenStorageService } from './token-storage.service';

const AUTH_API = '/api/auth/';
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loginStatus:boolean = false;

  ip:any;

  constructor(private http: HttpClient, private tokenStorage: TokenStorageService,) {}

  updateLoginStatus(status:boolean){
    this.loginStatus = status;
  }

  isLoggedIn(){
    return this.loginStatus;
  }

  // email can be used as alternative to username (backend accepts both)
  login(username: string, password: string): Observable<any> {

    // get client ip address and pass it to backend (along with the credentials)
    return this.http.get<{ip:string}>('https://jsonip.com').pipe(
      switchMap(data => {
        console.log('ip address', data.ip);
        this.ip = data.ip;
        return this.http.post(AUTH_API + 'signin/', JSON.stringify({
          username,
          password,
          'ip': this.ip,
        }), httpOptions);
      }),
      catchError(error => {
        this.ip = '';
        console.log(error);
        return this.http.post(AUTH_API + 'signin/', JSON.stringify({
          username,
          password,
          'ip': this.ip,
        }), httpOptions);
      }),
    );
  }

  // for user signup
  register(username: string, email: string, password: string, role: string): Observable<any> {

    return this.http.post(AUTH_API + 'signup/', JSON.stringify({
      username,
      email,
      password,
      role,
    }), httpOptions);
  }

  // only used (for user) to verify token, not validate
  verify(token: string): Observable<any> {
    return this.http.post(AUTH_API + 'verify/', JSON.stringify({
      token,
    }), httpOptions);
  }

  // refresh the access token as well as the refresh token
  refreshToken(): Observable<any> {
    var user = this.tokenStorage.getUser();
    var user_id = null
    if (user) {
      user_id = user.user_id
    }

    return this.http.post(AUTH_API + 'refresh/', JSON.stringify({ 'user_id': user_id }), httpOptions);
  }

  // handle authentication with google oauth2 on the backend
  googleAuth(idToken: string, authToken: string, role: string): Observable<any> {
    return this.http.post(AUTH_API + 'google/', JSON.stringify({ 'idToken': idToken, 'authToken': authToken, 'role': role }), httpOptions);
  }

  // handle authentication with facebook oauth2 on the backend
  facebookAuth(id: string, authToken: string, role: string): Observable<any> {
    return this.http.post(AUTH_API + 'facebook/', JSON.stringify({ 'id': id, 'authToken': authToken, 'role': role }), httpOptions);
  }

}