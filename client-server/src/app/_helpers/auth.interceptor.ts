import { HTTP_INTERCEPTORS, HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { TokenStorageService } from '../_services/token-storage.service';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, switchMap, filter, take, finalize, } from 'rxjs/operators';
import { AuthService } from '../_services/auth.service';
import { Router } from '@angular/router';

const TOKEN_HEADER_KEY = 'Authorization';
const LOGOUT_CODES = ['user_blocked', 'user_disabled', 'no_user_found', 'token_mismatch', 'refresh_token_missing', 'no_user_found'];

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(
    private router: Router,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
  ) { }

  /**
   * Intercepts all http request to attach access token to the header and handle error response flows
   * 
   * @param req - the http request
   * @param next - the http handler
   * @returns the BeahviourSubject containing the cloned request with appropriate headers
   */
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
        var err = error.error;
        // log user out if error message/error code indicates a need to reject the request
        if (err && (err.detail == "Token is invalid or expired" || (err.error && LOGOUT_CODES.includes(err.code)))) {
          this.logout();
          window.location.reload();
          //return throwError(error);
        } else if (!user || (user && !user.role)) {
          // propogate error for error catching and displays
          return throwError(error);
        }
        // otherwise refresh the access token using refresh token
        return this.handleTokenError(req, next);

      } else {
        return throwError(error);
      }
    }));
  }

  /**
   * Logs the user out
   */
  private logout(): void {
    this.tokenStorage.signOut();
  }

  /**
   * Add access token to the header
   * 
   * @param req - the http reequest
   * @param token - the user's access token
   * @returns the cloned request with proper headers
   */
  private addToken(req: HttpRequest<any>, token: string) {
    return req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, 'Bearer ' + token) });
  }

  /**
   * Handles 401, 403, 405 error (due to expired token) by attempting to refresh the tokens (assuming the old token expired)
   * while blocking all requests in between and retry after refresh returns
   * 
   * BehaviorSubject is used as a semaphore (to block and release requests during the refreshing)
   * 
   * @param request - the http request
   * @param next - the http handler
   * @returns the BehaviourSubject containing the cloned request with appropriate headers
   */
  private handleTokenError(request: HttpRequest<any>, next: HttpHandler) {

    // haven't start refreshing yet. Start refreshing
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshToken().pipe(
        finalize(() => this.isRefreshing = false),
        switchMap((token: any) => {
          this.tokenStorage.updateTokenAndUser(token.access);
          this.refreshTokenSubject.next(token.access);
          return next.handle(this.addToken(request, token.access));
        }),
        // refresh failed, logout
        catchError(error => {
          this.logout();
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
