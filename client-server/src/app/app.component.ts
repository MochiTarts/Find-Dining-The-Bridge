import { AfterViewInit, Component, OnInit } from '@angular/core';
import { UserService } from './_services/user.service';
import { SpinnerVisibilityService } from 'ng-http-loader';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { environment } from '../environments/environment';

declare let gtag: Function;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit {
  private role: string = 'BU';
  isLoggedIn = false;
  showROBoard = false;
  username?: string;

  constructor(
    private userService: UserService,
    private spinner: SpinnerVisibilityService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.spinner.show();
    if (!document.cookie.split('; ').find(row => row.startsWith('csrftoken'))) {
      this.userService.setCSRFToken().subscribe(
        data => {
        },
        err => {
        }
      )
    }

    /* This tracks the restaurant page views by BU and public users
    by adding the page path to google analytics for every time a BU or public user
    visits a restaurant page
    */
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        if (event.urlAfterRedirects.includes('restaurant?restaurantId')) {
          const restaurantId = event.urlAfterRedirects.split('?restaurantId=')[1]
          gtag('config', `${environment.googleAnalytics.trackingTag}`, {
            'page_title': "Restaurant Page Id="+restaurantId+" ("+`${environment.environment}`+")",
            'page_path': event.urlAfterRedirects
          });
        }
      }
    })

  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.spinner.hide();
    }, 1000)
  }

}
