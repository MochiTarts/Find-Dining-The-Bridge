import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { TokenStorageService } from '../_services/token-storage.service';
import { Location } from '@angular/common';
import { AuthService } from '../_services/auth.service';

@Injectable({ providedIn: 'root' })
export class ROGuard implements CanActivate {
    constructor(
        private router: Router,
        private tokenStorage: TokenStorageService,
        private authService: AuthService,
        private _location: Location,
    ) { }

    /**
     * This is a simple guard that just checks for RO rule
     * @returns boolean (true if user is RO; false otherwise)
     */
    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const user = this.tokenStorage.getUser();
        if (user && user.role == 'RO') {
            return true;
        } else {
            return new Observable<boolean>(obs => {

                this.authService.refreshToken().subscribe(
                    token => {
                        this.tokenStorage.updateTokenAndUser(token.access);
                        var user = this.tokenStorage.getUser();
                        this.authService.updateLoginStatus(true);
                        if (user && user.role == 'RO') {
                            obs.next(true);
                        } else {
                            // not a restaurant owner so go back to the previous page
                            this._location.back();
                            obs.next(false);
                        }
                    },
                    // refresh failed
                    err => {
                        // not a restaurant owner so go back to the previous page
                        this._location.back();
                        obs.next(false);
                    }
                );
            });
        }
    }
}