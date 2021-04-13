import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap, finalize } from 'rxjs/operators';
import { TokenStorageService } from './token-storage.service';

const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';
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

  constructor(private http: HttpClient, private tokenStorage: TokenStorageService,) {
    // Sets loginStatus to true if auth-token and auth-user keys are set and present
    if (window.sessionStorage.getItem(TOKEN_KEY) && window.sessionStorage.getItem(USER_KEY)) {
      this.loginStatus = true;
    }
  }

  /**
   * Sets loginStatus to status (true if user's logged in; false otherwise)
   * @param status - the login status of user
   */
  updateLoginStatus(status:boolean){
    this.loginStatus = status;
  }

  /**
   * Retrieves value of loginStatus
   * @returns boolean (loginStatus)
   */
  isLoggedIn(){
    return this.loginStatus;
  }

  /**
   * Performs action to log a user in
   * 
   * @param username - user's username or email
   * @param password - user's password
   * @returns the Observable from the login request
   */
  login(username: string, password: string): Observable<any> {

    // get client ip address and pass it to backend (along with the credentials)
    return this.http.get<{ip:string}>('https://jsonip.com').pipe(
      switchMap(data => {
        this.ip = data.ip;
        return this.http.post(AUTH_API + 'signin/', JSON.stringify({
          username,
          password,
          'ip': this.ip,
        }), httpOptions);
      }),
      catchError(error => {
        this.ip = '';
        return this.http.post(AUTH_API + 'signin/', JSON.stringify({
          username,
          password,
          'ip': this.ip,
        }), httpOptions);
      }),
    );
  }

  /**
   * Performs action for registering a new user
   * 
   * @param username - user's username
   * @param email - user's email
   * @param password - user's password
   * @param role - user's role
   * @returns the Observable from the signup request
   */
  register(username: string, email: string, password: string, role: string): Observable<any> {

    return this.http.post(AUTH_API + 'signup/', JSON.stringify({
      username,
      email,
      password,
      role,
    }), httpOptions);
  }

  /**
   * Performs action for resetting a user's password
   * 
   * @param email - user's email
   * @returns the Observable from password reset request
   */
  resetPasswordEmail(email: string): Observable<any>{
    return this.http.post(AUTH_API + 'password_reset/', JSON.stringify({
      email
    }), httpOptions);
  }

  /**
   * Performs action for resending verification email
   * 
   * @param email - user's email
   * @returns the Observable from resend verification email request
   */
  resendVerificationEmail(email: string): Observable<any>{
    return this.http.post(AUTH_API + 'resend_verification_email/', JSON.stringify({
      email
    }), httpOptions);
  }

  // only used (for user) to verify token, not validate
  /**
   * Verifies the user's access token
   * 
   * @param token - the user's access token
   * @returns the Observable from verifying a user's token
   */
  verify(token: string): Observable<any> {
    return this.http.post(AUTH_API + 'verify/', JSON.stringify({
      token,
    }), httpOptions);
  }

  /**
   * Retrieves a new token from Django backend
   * @returns the Observable from the refresh token request
   */
  refreshToken(): Observable<any> {
    var user = this.tokenStorage.getUser();
    var user_id = null
    if (user) {
      user_id = user.user_id
    }

    return this.http.post(AUTH_API + 'refresh/', JSON.stringify({ 'user_id': user_id }), httpOptions);
  }

  /**
   * Handles authentication with google oauth2 on the Django backend
   * PLEASE UPDATE DOCSTRING
   * 
   * @param idToken - ?
   * @param authToken - ?
   * @param role - the user's role
   * @returns the Observable from the google authentication request
   */
  googleAuth(idToken: string, authToken: string, role: string): Observable<any> {
    return this.http.post(AUTH_API + 'google/', JSON.stringify({ 'idToken': idToken, 'authToken': authToken, 'role': role }), httpOptions);
  }

  /**
   * Handles authentication with facebook oauth2 on the Django backend
   * PLEASE UPDATE DOCSTRING
   * 
   * @param id - ?
   * @param authToken - ? 
   * @param role - the user's role
   * @returns the Observable from the facebook authentication request
   */
  facebookAuth(id: string, authToken: string, role: string): Observable<any> {
    return this.http.post(AUTH_API + 'facebook/', JSON.stringify({ 'id': id, 'authToken': authToken, 'role': role }), httpOptions);
  }

}
