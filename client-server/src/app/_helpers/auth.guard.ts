import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { TokenStorageService } from '../_services/token-storage.service';
import { AuthService } from '../_services/auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(
        private router: Router,
        private authService: AuthService,
        private tokenStorage: TokenStorageService
    ) { }

    /**
     * This is the basic guard that just checks for any user (both BU and RO)
     * @returns boolean (true if user has a role; false otherwise)
     */
    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const user = this.tokenStorage.getUser();

        if (user && ['BU', 'RO'].includes(user.role)) {
            return true;
        } else {
            return new Observable<boolean>(obs => {

                this.authService.refreshToken().subscribe(
                    token => {
                        this.tokenStorage.updateTokenAndUser(token.access);
                        var user = this.tokenStorage.getUser();
                        if (user && ['BU', 'RO'].includes(user.role)) {
                            this.authService.updateLoginStatus(true);
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
        }
    }
}