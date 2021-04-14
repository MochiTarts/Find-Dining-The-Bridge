import {
  AfterViewInit,
  Component,
  OnInit,
  ViewChild,
} from '@angular/core';
import 'aos/dist/aos.css';
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import { HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { Title } from '@angular/platform-browser';
import { RestaurantService } from '../../_services/restaurant.service';
import { SubscriberProfileFormComponent } from 'src/app/components/subscriber-profile-form/subscriber-profile-form.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, AfterViewInit {
  publicContent?: string;

  role: string = '';
  email: string = '';
  userId: string = '';
  profileId: string = '';
  username: string = '';
  idToken: string = '';
  siteKey: string;
  loggedOut: boolean = true;

  faMapMarkerAlt = faMapMarkerAlt;

  arrowsOutside = window.innerWidth < 1020 ? false : true;

  modalRef: any;
  @ViewChild('userInfo') userInfo: SubscriberProfileFormComponent;

  restaurants: any[] = [];
  pricepoints: any[] = [];

  formBuilder: any;

  photoCourtesy: string = 'Restaurant A';
  spotlight: any;
  spotlightStory: string = "";

  location: string = '';
  find: string = '';

  constructor(
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private restaurantService: RestaurantService,
    private router: Router,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Home | Find Dining Scarborough");

    this.pricepoints = [
      { key: "$", value: "LOW" },
      { key: "$$", value: "MID" },
      { key: "$$$", value: "HIGH" },
      { key: "$$$$", value: "EXHIGH" }
    ]

    this.publicContent = "public content";
    if (this.authService.isLoggedIn) {
      this.loggedOut = false;
      const user = this.tokenStorageService.getUser();
      this.role = user.role;
      this.username = user.username;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;
    }

    this.getRestaurants();
  }

  ngAfterViewInit(): void {
    if (this.role && this.role == 'BU' && this.profileId == null) {
      this.userInfo.open(false);
    }
  }

  gotoRegister(): void {
    this.router.navigate(['/login']);
  }

  /**
   * Retreives all approved restaurants from database
   * and shuffles their order for carousel display as well
   * as pick a random restaurant for spotlight display
   */
  getRestaurants() {
    this.restaurantService.listRestaurants().subscribe((data) => {
      // Shuffle the order of restaurants
      this.shuffle(data.Restaurants)
      for (let restaurant of data.Restaurants) {
        let price = this.getPricepoint(String(restaurant.pricepoint));
        this.restaurants.push({
          type: 'restaurant',
          name: restaurant.name,
          cuisinePrice: restaurant.cuisines[0] + " - " + price,
          imgUrl: restaurant.logo_url,
          _id: restaurant._id
        });
      }

      // Pick a random restaurant for spotlight
      this.spotlight = data.Restaurants[0];

      // Set spotlight story and only display first 500 characters
      this.spotlightStory = this.spotlight.bio;
      if (this.spotlightStory.length > 500) {
        var str = this.spotlightStory.substr(0, 498);
        var wordIndex = str.lastIndexOf(" ");
        this.spotlightStory = str.substr(0, wordIndex) + '...';
      }
    });
  }

  /**
   * Retrieves the user-friendly values for each
   * price level
   * @param priceLevel - the price level (LOW, MID, HIGH, EXHIGH)
   * @returns
   */
  getPricepoint(priceLevel: string) {
    // priceLevels: LOW, MID, HIGH, EXHIGH
    // return: $, $$, $$$, $$$$
    for (let p of this.pricepoints) {
      if (p["value"] == priceLevel) {
        return p["key"];
      }
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.arrowsOutside = window.innerWidth < 1020 ? false : true;
  }

  browseListings(): void {
    this.router.navigate(['/all-listings']);
  }

  /**
   * Shuffles the list of restaurants
   * @param list - list of restaurants
   * @returns list of restaurants in new random order
   */
  shuffle(list: any[]) {
    // Reference: https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array

    var currentIndex = list.length, temporaryValue, randomIndex;

    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = list[currentIndex];
      list[currentIndex] = list[randomIndex];
      list[randomIndex] = temporaryValue;
    }

    return list;
  }
}
