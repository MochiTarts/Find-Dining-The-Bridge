'use strict';


customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">client-server documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                        <li class="link">
                            <a href="overview.html" data-type="chapter-link">
                                <span class="icon ion-ios-keypad"></span>Overview
                            </a>
                        </li>
                        <li class="link">
                            <a href="index.html" data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>README
                            </a>
                        </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                    </ul>
                </li>
                    <li class="chapter modules">
                        <a data-type="chapter-link" href="modules.html">
                            <div class="menu-toggler linked" data-toggle="collapse" ${ isNormalMode ?
                                'data-target="#modules-links"' : 'data-target="#xs-modules-links"' }>
                                <span class="icon ion-ios-archive"></span>
                                <span class="link-name">Modules</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                        </a>
                        <ul class="links collapse " ${ isNormalMode ? 'id="modules-links"' : 'id="xs-modules-links"' }>
                            <li class="link">
                                <a href="modules/AppModule.html" data-type="entity-link">AppModule</a>
                                    <li class="chapter inner">
                                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ?
                                            'data-target="#components-links-module-AppModule-1688e2e44096fe0e8d1cd6ece1986d34"' : 'data-target="#xs-components-links-module-AppModule-1688e2e44096fe0e8d1cd6ece1986d34"' }>
                                            <span class="icon ion-md-cog"></span>
                                            <span>Components</span>
                                            <span class="icon ion-ios-arrow-down"></span>
                                        </div>
                                        <ul class="links collapse" ${ isNormalMode ? 'id="components-links-module-AppModule-1688e2e44096fe0e8d1cd6ece1986d34"' :
                                            'id="xs-components-links-module-AppModule-1688e2e44096fe0e8d1cd6ece1986d34"' }>
                                            <li class="link">
                                                <a href="components/AboutUsComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">AboutUsComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/AccountSettingComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">AccountSettingComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/AllRestaurantsComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">AllRestaurantsComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/AppComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">AppComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ArticleCommonCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">ArticleCommonCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ArticleHeadlineCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">ArticleHeadlineCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/CarouselWithThumbnailComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">CarouselWithThumbnailComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/DishCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">DishCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/DynamicLabelComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">DynamicLabelComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/EditPostsComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">EditPostsComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/FavouritesComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">FavouritesComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/FilterdateCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">FilterdateCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/FilterlistCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">FilterlistCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/FooterComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">FooterComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/GetInvolvedComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">GetInvolvedComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/HomeComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">HomeComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/InfoCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">InfoCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/IvyCarouselComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">IvyCarouselComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/LoginComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">LoginComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/MapComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">MapComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/MenuEditComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">MenuEditComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/MultiselectCheckboxDropdownComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">MultiselectCheckboxDropdownComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/NavbarComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">NavbarComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/NewsArticlesComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">NewsArticlesComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/NewsletterComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">NewsletterComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/NewsletterSignupComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">NewsletterSignupComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/PageErrorComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">PageErrorComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/PartnerCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">PartnerCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/PasswordChangeFormComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">PasswordChangeFormComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/PostComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">PostComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/PrivacyPolicyComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">PrivacyPolicyComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ProfileComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">ProfileComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RequiredStarComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">RequiredStarComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ResourcesComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">ResourcesComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RestaurantCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">RestaurantCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RestaurantNearbyCardComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">RestaurantNearbyCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RestaurantPageComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">RestaurantPageComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RestaurantSetupComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">RestaurantSetupComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/SubscriberProfileFormComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">SubscriberProfileFormComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/TermsOfServiceComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">TermsOfServiceComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ThankyouPageComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">ThankyouPageComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/VirtualScrollingComponent.html"
                                                    data-type="entity-link" data-context="sub-entity" data-context-id="modules">VirtualScrollingComponent</a>
                                            </li>
                                        </ul>
                                    </li>
                            </li>
                            <li class="link">
                                <a href="modules/AppRoutingModule.html" data-type="entity-link">AppRoutingModule</a>
                            </li>
                </ul>
                </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#classes-links"' :
                            'data-target="#xs-classes-links"' }>
                            <span class="icon ion-ios-paper"></span>
                            <span>Classes</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="classes-links"' : 'id="xs-classes-links"' }>
                            <li class="link">
                                <a href="classes/Carousel.html" data-type="entity-link">Carousel</a>
                            </li>
                            <li class="link">
                                <a href="classes/dishValidator.html" data-type="entity-link">dishValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/draftValidator.html" data-type="entity-link">draftValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/formValidation.html" data-type="entity-link">formValidation</a>
                            </li>
                            <li class="link">
                                <a href="classes/formValidator.html" data-type="entity-link">formValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/generalUtils.html" data-type="entity-link">generalUtils</a>
                            </li>
                            <li class="link">
                                <a href="classes/geolocation.html" data-type="entity-link">geolocation</a>
                            </li>
                            <li class="link">
                                <a href="classes/linkValidator.html" data-type="entity-link">linkValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/newsletterValidator.html" data-type="entity-link">newsletterValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/ownerValidator.html" data-type="entity-link">ownerValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/passwordValidator.html" data-type="entity-link">passwordValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/postValidator.html" data-type="entity-link">postValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/restaurantValidator.html" data-type="entity-link">restaurantValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/signupValidator.html" data-type="entity-link">signupValidator</a>
                            </li>
                            <li class="link">
                                <a href="classes/Touches.html" data-type="entity-link">Touches</a>
                            </li>
                            <li class="link">
                                <a href="classes/userValidator.html" data-type="entity-link">userValidator</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#injectables-links"' :
                                'data-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/ArticleService.html" data-type="entity-link">ArticleService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/AuthService.html" data-type="entity-link">AuthService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/EmailService.html" data-type="entity-link">EmailService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/MediaService.html" data-type="entity-link">MediaService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/PostService.html" data-type="entity-link">PostService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/RestaurantService.html" data-type="entity-link">RestaurantService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/TokenStorageService.html" data-type="entity-link">TokenStorageService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/UserService.html" data-type="entity-link">UserService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#interceptors-links"' :
                            'data-target="#xs-interceptors-links"' }>
                            <span class="icon ion-ios-swap"></span>
                            <span>Interceptors</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="interceptors-links"' : 'id="xs-interceptors-links"' }>
                            <li class="link">
                                <a href="interceptors/AuthInterceptor.html" data-type="entity-link">AuthInterceptor</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#guards-links"' :
                            'data-target="#xs-guards-links"' }>
                            <span class="icon ion-ios-lock"></span>
                            <span>Guards</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="guards-links"' : 'id="xs-guards-links"' }>
                            <li class="link">
                                <a href="guards/AuthGuard.html" data-type="entity-link">AuthGuard</a>
                            </li>
                            <li class="link">
                                <a href="guards/ROGuard.html" data-type="entity-link">ROGuard</a>
                            </li>
                            <li class="link">
                                <a href="guards/SecureGuard.html" data-type="entity-link">SecureGuard</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#interfaces-links"' :
                            'data-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/ActiveSlides.html" data-type="entity-link">ActiveSlides</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Image.html" data-type="entity-link">Image</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Images.html" data-type="entity-link">Images</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Properties.html" data-type="entity-link">Properties</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Properties-1.html" data-type="entity-link">Properties</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#miscellaneous-links"'
                            : 'data-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/enumerations.html" data-type="entity-link">Enums</a>
                            </li>
                            <li class="link">
                                <a href="miscellaneous/typealiases.html" data-type="entity-link">Type aliases</a>
                            </li>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <a data-type="chapter-link" href="routes.html"><span class="icon ion-ios-git-branch"></span>Routes</a>
                        </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
                    <li class="divider"></li>
                    <li class="copyright">
                        Documentation generated using <a href="https://compodoc.app/" target="_blank">
                            <img data-src="images/compodoc-vectorise.png" class="img-responsive" data-type="compodoc-logo">
                        </a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});