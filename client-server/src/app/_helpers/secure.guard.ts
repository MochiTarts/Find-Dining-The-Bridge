import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';

import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from '../_services/token-storage.service';

@Injectable({ providedIn: 'root' })
export class SecureGuard implements CanActivate {
    constructor(
        private router: Router,
        private authService: AuthService,
        private tokenStorage: TokenStorageService,
    ) { }
    // this is the most secured guard that will verify the refresh token on the backend against the database
    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {

        if (this.authService.isLoggedIn()){
            return new Observable<boolean>(obs => {

                this.authService.refreshToken().subscribe(
                    token => {
                        this.tokenStorage.updateTokenAndUser(token.access);
                        var user = this.tokenStorage.getUser();
                        if (user && ['BU', 'RO'].includes(user.role)) {
                            obs.next(true);
                        } else{
                            // not logged in so redirect to login page with the return url
                            this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
                            obs.next(false);
                        }
                    },
                    // refresh failed
                    err => {
                        // not logged in so redirect to login page with the return url
                        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
                        obs.next(false);
                    }
                );
                });
        } else {
            return false;
        }






    }
}
