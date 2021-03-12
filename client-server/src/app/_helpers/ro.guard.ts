import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { TokenStorageService } from '../_services/token-storage.service';
import { Location } from '@angular/common';

@Injectable({ providedIn: 'root' })
export class ROGuard implements CanActivate {
    constructor(
        private router: Router,
        private tokenStorage: TokenStorageService,
        private _location: Location,
    ) { }
    // this is a simple guard that just checks for RO rule
    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        const user = this.tokenStorage.getUser();
        if (user && user.role == 'RO') {
            return true;
        }

        // not a restaurant owner so go back to the previous page
        this._location.back();
        // this.router.navigate([state.url]);
        return false;
    }
}