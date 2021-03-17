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
    //console.log(token);
    // add access token to the header
    if (token != null) {
      authReq = this.addToken(req, token);
    }

    return next.handle(authReq).pipe(catchError(error => {
      console.log(error);
      if (error instanceof HttpErrorResponse && [401, 403].includes(error.status)) {
        console.log(error.error);
        // determine the source of 401 error
        if (!this.isCheckingRefreshToken && error.status === 401) {
          // the current request is for refreshing tokens (and not to log user out)
          if (error.error && error.error.code == "token_not_valid"){
            this.isCheckingRefreshToken = true;
            // the current request is due to a fail login
          } else if (!this.tokenStorage.getUser().role){
            // propogate error for error catching and displays
            return throwError(error);
          }
        }
        // auto logout if refresh token expired or 403 response returned from api
        if (this.isCheckingRefreshToken || error.status === 403 && this.tokenStorage.getUser()) {
          this.isCheckingRefreshToken = false;
          this.logout();
          //this.router.navigate(['login']);
        }
        // otherwise refresh the access token using refresh token
        return this.handle401Error(req, next);
        // log user out if 400 and error code indicates a need to reject the request
      } else if (error instanceof HttpErrorResponse && error.status === 400) {
        if (error.error && ['no_valid_token_in_db', 'no_user_found', 'user_disabled', 'user_blocked'].includes(error.error.code)) {
          console.log(error.error);
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
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshToken().pipe(
        switchMap((token: any) => {
          console.log(token);
          this.isRefreshing = false;
          this.refreshTokenSubject.next(token.access);
          this.tokenStorage.updateTokenAndUser(token.access);
          return next.handle(this.addToken(request, token.access));
        }),
        catchError(error => {
          console.log(error.error);
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
          console.log(error.error);
          return throwError(error);
        }));
    }
  }
}

export const authInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
];