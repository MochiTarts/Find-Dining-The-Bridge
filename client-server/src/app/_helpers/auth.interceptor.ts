import { HTTP_INTERCEPTORS, HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { TokenStorageService } from '../_services/token-storage.service';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, switchMap, filter, take, } from 'rxjs/operators';
import { AuthService } from '../_services/auth.service';
import { Router } from '@angular/router';

const TOKEN_HEADER_KEY = 'Authorization';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private isCheckingRefreshToken = false;
  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(private router: Router, private authService: AuthService, private tokenStorage: TokenStorageService) { }
  // intercepts all http request to attach access token to the header and handle error response flows
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let authReq = req;
    const token = this.tokenStorage.getToken();
    // add access token to the header
    if (token != null) {
      authReq = this.addToken(req, token);
    }

    return next.handle(authReq).pipe(catchError(error => {
      if (error instanceof HttpErrorResponse && [401, 403, 405].includes(error.status)) {

        var user = this.tokenStorage.getUser();
        /*
        // determine the source of 401/403 error (401 from readonly or 403 from isAuthenticated)
        if (!this.isCheckingRefreshToken) {
          // the current request is for refreshing tokens (and not to log user out)
          if (error.error && error.error.code == "token_not_valid"){
            this.isCheckingRefreshToken = true;
            // the current request is due to a fail login
          } else if (!user || !user.role){
            // propogate error for error catching and displays
            return throwError(error);
          }
        }
        // auto logout if refresh token expired or 403 response returned from api
        //if (this.isCheckingRefreshToken || error.status === 403 && this.tokenStorage.getUser()) {
        else if (this.isCheckingRefreshToken) {
          //this.isCheckingRefreshToken = false;
          //this.logout();
          //this.router.navigate(['login']);
        }
        */
       var err = error.error;
       if (err && err.detail == "Token is invalid or expired"){
         this.logout();
         return throwError(error);
       } else if (!user && !user.role){
          // propogate error for error catching and displays
          return throwError(error);
       }
        // otherwise refresh the access token using refresh token
        return this.handle401Error(req, next);
        // log user out if 400 and error code indicates a need to reject the request
      } else if (error instanceof HttpErrorResponse && error.status === 400) {
        if (error.error && ['no_valid_token_in_db', 'no_user_found', 'user_disabled', 'user_blocked'].includes(error.error.code)) {
          this.logout();
          return throwError(error);
          // 400 example: duplicate username/email on signup
        } else {
          return throwError(error);
        }
      } else {
        return throwError(error);
      }
    }));
  }

  private logout(): void {
    this.tokenStorage.signOut();
    window.location.reload();
  }

  // add access token to the header
  private addToken(req: HttpRequest<any>, token: string) {
    return req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, 'Bearer ' + token) });
  }

  /*
  Handles 401 error by attempting to refresh the tokens (assuming the old token expired)
  while blocking all requests in between and retry after refresh returns

  BehaviorSubject is used as a semaphore (to block and release requests during the refreshing)
  */
  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {

    // haven't start refreshing yet. Start refreshing
    if (!this.isRefreshing) {
    //if (this.isCheckingRefreshToken) {

      this.isRefreshing = true;
      //this.isCheckingRefreshToken = false;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshToken().pipe(
        switchMap((token: any) => {
          this.isRefreshing = false;
          //this.isCheckingRefreshToken = true;
          this.tokenStorage.updateTokenAndUser(token.access);
          this.refreshTokenSubject.next(token.access);
          return next.handle(this.addToken(request, token.access));
        }),
        catchError(error => {
          return throwError(error);
        }),
      );
      // refreshing, block the request until token is not null (refreshTokenSubject contains a not null value)
    } else {
      return this.refreshTokenSubject.pipe(
        filter(token => token != null),
        take(1),
        switchMap(JWT => {
          return next.handle(this.addToken(request, JWT));
        }),
        catchError(error => {
          return throwError(error);
        }));
    }
  }
}

export const authInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
];
