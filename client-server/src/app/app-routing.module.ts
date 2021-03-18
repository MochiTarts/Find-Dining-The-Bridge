import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { BoardUserComponent } from './board-user/board-user.component';
import { BoardROComponent } from './board-ro/board-ro.component';
import { AuthGuard } from './_helpers/auth.guard';
import { SecureGuard } from './_helpers/secure.guard';
import { ROGuard } from './_helpers/ro.guard';
import {AccountSettingComponent} from './account-setting/account-setting.component';
import { FavouritesComponent } from './favourites/favourites.component';
import { AllRestaurantsComponent } from './all-restaurants/all-restaurants.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [SecureGuard] },
  { path: 'user', component: BoardUserComponent, canActivate: [AuthGuard] },
  { path: 'ro', component: BoardROComponent, canActivate: [ROGuard] },
  { path: 'account-setting', component: AccountSettingComponent, canActivate: [AuthGuard]},
  { path: 'all-listings', component: AllRestaurantsComponent, canActivate: [AuthGuard] },
  { path: 'favourites', component: FavouritesComponent, canActivate: [AuthGuard] },
  /*
  { path: 'verification', component: EmptyComponent, children: [
    {
      path: '**',
      component: EmptyComponent,
    }
  ]},
  */
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled', // Add options right here
  }),],
  exports: [RouterModule]
})
export class AppRoutingModule { }