import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './_helpers/auth.guard';
import { SecureGuard } from './_helpers/secure.guard';
import { ROGuard } from './_helpers/ro.guard';

import { LoginComponent } from './pages/login/login.component'
import { HomeComponent } from './pages/home/home.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { AccountSettingComponent } from './pages/account-setting/account-setting.component';
import { NewsletterComponent } from './pages/newsletter/newsletter.component';
import { FavouritesComponent } from './pages/favourites/favourites.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';
import { RestaurantSetupComponent } from './pages/restaurant-setup/restaurant-setup.component';
import { TermsOfServiceComponent } from './pages/terms-of-service/terms-of-service.component';
import { RestaurantPageComponent } from './pages/restaurant-page/restaurant-page.component';
import { EditPostsComponent } from './pages/posts-edit/edit-posts.component';
import { MenuEditComponent } from './pages/menu-edit/menu-edit.component';
import { GetInvolvedComponent } from './pages/get-involved/get-involved.component';
import { NewsArticlesComponent } from './pages/news-articles/news-articles.component';
import { PrivacyPolicyComponent } from './pages/privacy-policy/privacy-policy.component';
import { AboutUsComponent } from './pages/about-us/about-us.component';
import { ResourcesComponent } from './pages/resources/resources.component';
import { NewsletterSignupComponent } from './pages/newsletter-signup/newsletter-signup.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'account-setting', component: AccountSettingComponent, canActivate: [AuthGuard] },
  { path: 'newsletter', component: NewsletterComponent, canActivate: [AuthGuard] },
  { path: 'all-listings', component: AllRestaurantsComponent },
  { path: 'favourites', component: FavouritesComponent, canActivate: [AuthGuard] },
  { path: 'restaurant-setup', component: RestaurantSetupComponent, canActivate: [AuthGuard, ROGuard] },
  { path: 'terms-of-service', component: TermsOfServiceComponent },
  { path: 'restaurant', component: RestaurantPageComponent },
  { path: 'edit-posts', component: EditPostsComponent, canActivate: [AuthGuard, ROGuard] },
  { path: 'menu-edit', component: MenuEditComponent, canActivate: [AuthGuard, ROGuard] },
  { path: 'get-involved', component: GetInvolvedComponent, },
  { path: 'articles', component: NewsArticlesComponent, },
  { path: 'privacy-policy', component: PrivacyPolicyComponent, },
  { path: 'about-us', component: AboutUsComponent, },
  { path: 'resources', component: ResourcesComponent, canActivate: [AuthGuard, ROGuard] },
  { path: 'newsletter-signup', component: NewsletterSignupComponent, },
  /*
  { path: 'verification', component: EmptyComponent, children: [
    {
      path: '**',
      component: EmptyComponent,
    }
  ]},
  */
  { path: '', redirectTo: '', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled', // Add options right here
  }),],
  exports: [RouterModule]
})
export class AppRoutingModule { }
