import {
  AfterViewInit,
  TemplateRef,
  Component,
  OnInit,
  ViewChild
} from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { FormGroup, Validators } from '@angular/forms';
import { faArrowCircleDown, faArrowCircleUp, faCalendar } from '@fortawesome/free-solid-svg-icons';
import { formValidator } from '../../_validation/formValidator'
import { userValidator } from '../../_validation/userValidator';
import { UserService } from '../../_services/user.service';
import { HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { environment } from 'src/environments/environment';
import { SubscriberProfileFormComponent } from 'src/app/components/subscriber-profile-form/subscriber-profile-form.component';
import { RestaurantCardComponent } from 'src/app/components/restaurant-card/restaurant-card.component';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { RestaurantProfileFormComponent } from 'src/app/components/restaurant-profile-form/restaurant-profile-form.component';

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

  @ViewChild('userInfo') userInfo: SubscriberProfileFormComponent;
  @ViewChild('restaurantInfo') restaurantInfo: RestaurantProfileFormComponent;

  isShow: boolean;
  topPosToStartShowing = 100;
  faArrowCircleUp = faArrowCircleUp;
  faArrowCircleDown = faArrowCircleDown;
  arrowsOutside = true;
  faCalendar = faCalendar;
  
  modalRef: any;

  totalStars: number = 5;
  dishes: any[] = [];
  stories: any[] = [];

  cuisines = [
    {
      type: 'image',
      path: 'assets/images/cuisines/chinese.jpg',
      caption: 'Chinese',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/greek.jpg',
      caption: 'Greek',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/indian.jpg',
      caption: 'Indian',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/italian.jpg',
      caption: 'Italian',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/japanese.jpg',
      caption: 'Japanese',
    },
    { type: 'image', path: 'assets/images/cuisines/thai.jpg', caption: 'Thai' },
    {
      type: 'image',
      path: 'assets/images/cuisines/vietnamese.jpg',
      caption: 'Vietnamese',
    },
  ];
  formBuilder: any;

  constructor(
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private userService: UserService,
    private modalService: NgbModal,
    private router: Router
    ) { }

  ngOnInit(): void {
    AOS.init({
      delay: 300,
      duration: 1500,
      once: false,
      anchorPlacement: 'top-bottom',
    });
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
  }

  ngAfterViewInit(): void {
    // Add one more '&&' statement to see if profile_id is null
    if (this.role && this.role == 'BU' && this.profileId == null) {
      this.userInfo.open(false);
    } else if (this.role && this.role == 'RO') {
      this.restaurantInfo.open(false);
    }
  }

  @HostListener('window:scroll')
  checkScroll() {
    const scrollPosition =
      window.pageYOffset ||
      document.documentElement.scrollTop ||
      document.body.scrollTop ||
      0;

    if (scrollPosition >= this.topPosToStartShowing) {
      this.isShow = true;
    } else {
      this.isShow = false;
    }
  }

  gotoTop() {
    window.scroll({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  }

  scrollDown() {
    const newPosition = document.getElementById('scroll').offsetTop;
    window.scroll({
      top: newPosition,
      left: 0,
      behavior: 'smooth',
    });
  }

  onLoginRegisterClicked(): void {
    this.router.navigate(['/login']);
  }

  browseListings(): void {
    this.router.navigate(['/all-listings']);
  }

  restaurant(): void {}

  browseStories(): void {}
}