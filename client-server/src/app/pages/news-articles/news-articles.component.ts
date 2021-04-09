import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { faSearch, faStar } from '@fortawesome/free-solid-svg-icons';
import { ArticleService } from '../../_services/article.service';
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { RestaurantService } from 'src/app/_services/restaurant.service';
import { SubscriberProfileFormComponent } from 'src/app/components/subscriber-profile-form/subscriber-profile-form.component';
import { AuthService } from 'src/app/_services/auth.service';

@Component({
  selector: 'app-news-articles',
  templateUrl: './news-articles.component.html',
  styleUrls: ['./news-articles.component.scss']
})
export class NewsArticlesComponent implements OnInit {
  role: string = '';
  profileId: string = '';

  /*
  Array containing all viewable articles
  Will not update upon being filtered
  Is meant to be used as a set list of all viewable articles
  to prevent constant calling of get articles endpoint
  */
  allArticles: any[];

  months: any[];
  years: any[] = [];
  dark = "dark";

  /*
  Array that contains all articles viewable and filtered
  Will always update to contain the articles according
  to the filter option(s)
  */
  filteredArticles: any[] = [];
  latestArticles: any[] = [];

  filterMonthArticles: any[];
  filterYearArticles: any[];

  faSearch = faSearch;
  faStar = faStar;

  selectedArticle: any = Object;
  totalTabs: any[] = [];

  @ViewChild('userInfo') userInfo: SubscriberProfileFormComponent;

  constructor(
    public articleService: ArticleService,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
    private titleService: Title,
  ) {
    this.months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    var currentYear = new Date().getFullYear()
    var minYear = currentYear - 5 // Subject to change
    for (var year = currentYear; year >= minYear; year--) {
      this.years.push(year);
    }
  }

  ngOnInit(): void {
    this.titleService.setTitle("Articles | Find Dining Scarborough");
    AOS.init({
      delay: 300,
      duration: 1500,
      once: true,
      anchorPlacement: 'top-bottom',
    });

    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.profileId = user.profile_id;
    }

    this.articleService.getArticles().subscribe((data) => {
      this.allArticles = data.articles;
      this.filteredArticles = data.articles;

      for (let i = 0; i < this.allArticles.length; i++) {
        this.filteredArticles[i].type = 'article';
      }
      this.latestArticles = this.filteredArticles.slice(0, 8);

      this.selectedArticle = this.filteredArticles[1];
      length = Math.ceil(this.filteredArticles.length/10);
      this.totalTabs = Array(length);
    })
  }

  ngAfterViewInit(): void {
    if (this.role && this.role == 'BU' && this.profileId == null) {
      this.userInfo.open(false);
    }
  }

  openArticle(article) {
    this.selectedArticle = article;

    var articleListDiv = document.getElementById("article-list");
    articleListDiv.style.display = "none";
    articleListDiv.style.opacity = "0";

    var articleDiv = document.getElementById("article-container");
    articleDiv.style.display = "block";
    setTimeout(() => {
      articleDiv.style.opacity = "1";
    }, 10);
  }

  closeArticle() {
    var articleDiv = document.getElementById("article-container");
    articleDiv.style.display = "none";
    articleDiv.style.opacity = "0";

    var articleListDiv = document.getElementById("article-list");
    articleListDiv.style.display = "block";
    setTimeout(() => {
      articleListDiv.style.opacity = "1";
    }, 10);
  }

  openArticleMobile(article) {
    this.selectedArticle = article;

    var articleListDiv = document.getElementById("article-list-mobile");
    articleListDiv.style.display = "none";
    articleListDiv.style.opacity = "0";

    var articleDiv = document.getElementById("article-container-mobile");
    articleDiv.style.display = "block";
    setTimeout(() => {
      articleDiv.style.opacity = "1";
    }, 10);
  }

  closeArticleMobile() {
    var articleDiv = document.getElementById("article-container-mobile");
    articleDiv.style.display = "none";
    articleDiv.style.opacity = "0";

    var articleListDiv = document.getElementById("article-list-mobile");
    articleListDiv.style.display = "block";
    setTimeout(() => {
      articleListDiv.style.opacity = "1";
    }, 10);
  }

  toggleFilter() {
    var mobileFilterDiv = document.getElementById("mobile-filter");

    if (mobileFilterDiv.style.opacity === "0") {
      mobileFilterDiv.style.opacity = "1";
      mobileFilterDiv.style.marginRight = "0";
    } else {
      mobileFilterDiv.style.opacity = "0";
      mobileFilterDiv.style.marginRight = "-400px";
    }
  }

  filterEnter(event){
    event.srcElement.click();
  }

  filterDate(map) {
    const isFalse = (currentValue) => !currentValue;

    var monthList = map.month;
    var yearList = map.year;

    this.filterMonthArticles = [];
    this.filterYearArticles = [];

    if (monthList.every(isFalse) && yearList.every(isFalse)) {
      // If every option is unchecked
      this.filteredArticles = this.allArticles;
    } else {
      // If some option(s) are checked
      for (let article of this.allArticles) {
        if (monthList.every(isFalse)) {
          this.filterMonthArticles = this.allArticles;
        } else {
          var date = new Date(article.modified_at);
          var monthNumber = date.getMonth();
          for (var i = 0; i < this.months.length; i++) {
            if (monthList[i] && i == monthNumber) {
              this.filterMonthArticles.push(article)
            }
          }
        }

        if (yearList.every(isFalse)) {
          this.filterYearArticles = this.allArticles;
        } else {
          var date = new Date(article.modified_at);
          var year = date.getFullYear();
          for (var i = 0; i < this.years.length; i++) {
            if (yearList[i] && this.years[i] == year) {
              this.filterYearArticles.push(article);
            }
          }
        }
      }

      this.filteredArticles = [];
      for (let article of this.allArticles) {
        if (this.filterMonthArticles.includes(article) && this.filterYearArticles.includes(article)) {
          this.filteredArticles.push(article);
        }
      }
    }

    this.latestArticles = this.filteredArticles;
  }

  seeAll() {
    this.filteredArticles = this.allArticles;
    this.latestArticles = this.allArticles;
  }

  seeMostRecent() {
    this.filteredArticles = this.allArticles.slice(0, 8);
    this.latestArticles = this.allArticles.slice(0, 8);
  }

}
