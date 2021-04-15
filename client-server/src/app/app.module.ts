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
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';

import { CarouselModule } from 'ngx-bootstrap/carousel';
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
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';

import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { NewsletterComponent } from './pages/newsletter/newsletter.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';
import { FavouritesComponent } from './pages/favourites/favourites.component';
import { RestaurantSetupComponent } from './pages/restaurant-setup/restaurant-setup.component';
import { TermsOfServiceComponent } from './pages/terms-of-service/terms-of-service.component';
import { RestaurantPageComponent } from './pages/restaurant-page/restaurant-page.component';
import { EditPostsComponent } from './pages/posts-edit/edit-posts.component';
import { MenuEditComponent } from './pages/menu-edit/menu-edit.component';
import { GetInvolvedComponent } from './pages/get-involved/get-involved.component';
import { AccountSettingComponent } from './pages/account-setting/account-setting.component';
import { NewsArticlesComponent } from './pages/news-articles/news-articles.component';

import { IvyCarouselComponent } from './components/carousel/carousel.component';
import { CarouselWithThumbnailComponent } from './components/carousel-with-thumbnail/carousel-with-thumbnail.component';
import { DishCardComponent } from './components/dish-card/dish-card.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { FilterlistCardComponent } from './components/filterlist-card/filterlist-card.component';
import { MapComponent } from './components/map/map.component';
import { RestaurantCardComponent } from './components/restaurant-card/restaurant-card.component';
import { RestaurantNearbyCardComponent } from './components/restaurant-nearby-card/restaurant-nearby-card.component';
import { DynamicLabelComponent } from './components/dynamic-label/dynamic-label.component';
import { RequiredStarComponent } from './components/required-star/required-star.component';
import { SubscriberProfileFormComponent } from './components/subscriber-profile-form/subscriber-profile-form.component';
import { PageErrorComponent } from './components/page-error/page-error.component';
import { VirtualScrollingComponent } from './components/virtual-scrolling/virtual-scrolling.component';
import { PostComponent } from './components/post/post.component';
import { PartnerCardComponent } from './components/partner-card/partner-card.component';
import { MultiselectCheckboxDropdownComponent } from './components/multiselect-checkbox-dropdown/multiselect-checkbox-dropdown.component';
import { PasswordChangeFormComponent } from './components/password-change-form/password-change-form.component';
import { InfoCardComponent } from './components/info-card/info-card.component';
import { ArticleCommonCardComponent } from './components/article-common-card/article-common-card.component';
import { FilterdateCardComponent } from './components/filterdate-card/filterdate-card.component';
import { PrivacyPolicyComponent } from './pages/privacy-policy/privacy-policy.component';
import { AboutUsComponent } from './pages/about-us/about-us.component';
import { ArticleHeadlineCardComponent } from './components/article-headline-card/article-headline-card.component';


@NgModule({
  declarations: [
    AppComponent,
    IvyCarouselComponent,
    CarouselWithThumbnailComponent,
    DishCardComponent,
    LoginComponent,
    HomeComponent,
    ProfileComponent,
    NewsletterComponent,
    NavbarComponent,
    FooterComponent,
    AllRestaurantsComponent,
    FavouritesComponent,
    FilterlistCardComponent,
    MapComponent,
    RestaurantCardComponent,
    RestaurantNearbyCardComponent,
    RestaurantSetupComponent,
    DynamicLabelComponent,
    RequiredStarComponent,
    TermsOfServiceComponent,
    SubscriberProfileFormComponent,
    RestaurantPageComponent,
    PageErrorComponent,
    VirtualScrollingComponent,
    EditPostsComponent,
    PostComponent,
    MenuEditComponent,
    GetInvolvedComponent,
    PartnerCardComponent,
    MultiselectCheckboxDropdownComponent,
    PasswordChangeFormComponent,
    AccountSettingComponent,
    InfoCardComponent,
    NewsArticlesComponent,
    ArticleCommonCardComponent,
    FilterdateCardComponent,
    PrivacyPolicyComponent,
    AboutUsComponent,
    ArticleHeadlineCardComponent,
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
    MatSelectModule,
    MatFormFieldModule,
    MatProgressBarModule,
    MatDividerModule,
    NgxCaptchaModule,
    MatCardModule,
    MatButtonModule,
    CarouselModule.forRoot(),
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

