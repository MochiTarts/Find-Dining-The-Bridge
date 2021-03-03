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

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let authReq = req;
    const token = this.tokenStorage.getToken();
    //console.log(token);
    if (token != null) {
      authReq = this.addToken(req, token);
    }

    return next.handle(authReq).pipe(catchError(error => {
      if (error instanceof HttpErrorResponse && [401, 403].includes(error.status)) {
        console.log(error.error);
        if (!this.isCheckingRefreshToken && error.status === 401 && error.error && error.error.code == "token_not_valid"){
          this.isCheckingRefreshToken = true;
        }
        // auto logout if refresh token expired or 403 response returned from api
        if (this.isCheckingRefreshToken || error.status === 403 && this.tokenStorage.getUser()) {
          this.isCheckingRefreshToken = false;
          this.tokenStorage.signOut();
          this.router.navigate(['login']);
        }
        // otherwise refresh the access token using refresh token
        return this.handle401Error(req, next);
      } else {
        return throwError(error);
      }
    }));
  }

  private addToken(req: HttpRequest<any>, token: string) {
    return req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, 'Bearer ' + token) });
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshToken().pipe(
        switchMap((token: any) => {
          console.log(token);
          this.isRefreshing = false;
          this.refreshTokenSubject.next(token.access);
          this.tokenStorage.saveToken(token.access);
          return next.handle(this.addToken(request, token.access));
        }));

    } else {
      return this.refreshTokenSubject.pipe(
        filter(token => token != null),
        take(1),
        switchMap(JWT => {
          return next.handle(this.addToken(request, JWT));
        }));
    }
  }
}

export const authInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
];