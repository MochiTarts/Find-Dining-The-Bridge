import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { SocialLoginModule, SocialAuthServiceConfig } from 'angularx-social-login';
import {
  GoogleLoginProvider,
  FacebookLoginProvider
} from 'angularx-social-login';

import { NgHttpLoaderModule } from 'ng-http-loader';

import { authInterceptorProviders } from './_helpers/auth.interceptor';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MatTabsModule } from '@angular/material/tabs';
import { NgxCaptchaModule } from 'ngx-captcha';

import { NgMultiSelectDropDownModule } from "ng-multiselect-dropdown";
import { YouTubePlayerModule } from '@angular/youtube-player';
import { MatIconModule } from '@angular/material/icon';
import { FlexLayoutModule } from "@angular/flex-layout";
import { GalleryModule } from 'ng-gallery';
import { LightboxModule } from 'ng-gallery/lightbox';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatPasswordStrengthModule } from '@angular-material-extensions/password-strength';
import { MatInputModule } from '@angular/material/input';
import { MatProgressBarModule } from '@angular/material/progress-bar';

import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { BoardROComponent } from './board-ro/board-ro.component';
import { BoardUserComponent } from './board-user/board-user.component';
import { NewsletterComponent } from './newsletter/newsletter.component';

import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { AllRestaurantsComponent } from './all-restaurants/all-restaurants.component';
import { FavouritesComponent } from './favourites/favourites.component';
import { FilterlistCardComponent } from './filterlist-card/filterlist-card.component';
import { MapComponent } from './map/map.component';
import { RestaurantCardComponent } from './restaurant-card/restaurant-card.component';
import { RestaurantFavsCardComponent } from './restaurant-favs-card/restaurant-favs-card.component';
import { RestaurantNearbyCardComponent } from './restaurant-nearby-card/restaurant-nearby-card.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    ProfileComponent,
    BoardROComponent,
    BoardUserComponent,
    NewsletterComponent,
    NavbarComponent,
    FooterComponent,
    AllRestaurantsComponent,
    FavouritesComponent,
    FilterlistCardComponent,
    MapComponent,
    RestaurantCardComponent,
    RestaurantFavsCardComponent,
    RestaurantNearbyCardComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({ cookieName: 'csrftoken', headerName: 'X-CSRFToken' }),
    FormsModule,
    SocialLoginModule,
    NgHttpLoaderModule.forRoot(),
    ReactiveFormsModule,
    FontAwesomeModule,
    NgbModule,
    MatIconModule,
    MatTabsModule,
    MatInputModule,
    MatProgressBarModule,
    NgxCaptchaModule,
    NgMultiSelectDropDownModule.forRoot(),
    YouTubePlayerModule,
    FlexLayoutModule,
    GalleryModule,
    LightboxModule,
    ScrollingModule,
    MatPasswordStrengthModule.forRoot(),
  ],
  providers: [authInterceptorProviders, {
    provide: 'SocialAuthServiceConfig',
    useValue: {
      autoLogin: false,
      providers: [
        {
          id: GoogleLoginProvider.PROVIDER_ID,
          provider: new GoogleLoginProvider(
            '739217804766-54cq902bdq8s7qcghtu7a6b43qel9984.apps.googleusercontent.com'
          )
        },
        {
          id: FacebookLoginProvider.PROVIDER_ID,
          provider: new FacebookLoginProvider('874417486731218')
        }
      ]
    } as SocialAuthServiceConfig,
  },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

