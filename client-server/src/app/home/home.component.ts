import {
  AfterViewInit,
  TemplateRef,
  Component,
  OnInit,
  ViewChild
} from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { FormGroup } from '@angular/forms';
import { faArrowCircleDown, faArrowCircleUp, faCalendar } from '@fortawesome/free-solid-svg-icons';
import { formValidator } from '../validation/formValidator';
import { userValidator } from '../validation/userValidator';
import { UserService } from '../_services/user.service';
import { HostListener } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, AfterViewInit {
  publicContent?: string;

  role: string = '';
  userId: string = '';
  idToken: string = '';
  userData: any;
  siteKey: string;
  loggedOut: boolean = true;

  aFormGroup: FormGroup;
  validator: formValidator = new userValidator();

  isShow: boolean;
  topPosToStartShowing = 100;
  faArrowCircleUp = faArrowCircleUp;
  faArrowCircleDown = faArrowCircleDown;
  arrowsOutside = true;
  faCalendar = faCalendar;

  @ViewChild('userInfo', { static: true }) content: TemplateRef<any>;
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

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
    AOS.init({
      delay: 300,
      duration: 1500,
      once: false,
      anchorPlacement: 'top-bottom',
    });
    this.publicContent = "public content";
  }

  ngAfterViewInit(): void {
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

  browseListings(): void {}

  restaurant(): void {}

  browseStories(): void {}
}