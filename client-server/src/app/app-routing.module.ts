import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './_helpers/auth.guard';
import { SecureGuard } from './_helpers/secure.guard';
import { ROGuard } from './_helpers/ro.guard';

import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { AccountSettingComponent } from './pages/account-setting/account-setting.component';
import { NewsletterComponent } from './pages/newsletter/newsletter.component';
import { FavouritesComponent } from './pages/favourites/favourites.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'account-setting', component: AccountSettingComponent, canActivate: [AuthGuard] },
  { path: 'newsletter', component: NewsletterComponent },
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