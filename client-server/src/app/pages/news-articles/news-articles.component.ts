import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { faSearch, faStar, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
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
  faTimesCircle = faTimesCircle;

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
    this.titleService.setTitle("Media | Find Dining Scarborough");
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

      this.selectedArticle = this.filteredArticles[0];
      length = Math.ceil(this.filteredArticles.length/10);
      this.totalTabs = Array(length);
    })
  }

  ngAfterViewInit(): void {
  }

  /**
   * Sets the selectedArticle to the input article for display
   * Performs css transitions to display article instead of
   * articles headlines list
   * 
   * @param article - the article to open
   */
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

    let el = document.getElementById("article-container");
    el.scrollIntoView({
      behavior: 'smooth'
    });
  }

  /**
   * Performs css transitions to close selectedArticle and display
   * the articles headelins list again
   */
  closeArticle() {
    var articleDiv = document.getElementById("article-container");
    articleDiv.style.display = "none";
    articleDiv.style.opacity = "0";

    var articleListDiv = document.getElementById("article-list");
    articleListDiv.style.display = "flex";
    setTimeout(() => {
      articleListDiv.style.opacity = "1";
    }, 10);
  }

  /**
   * The mobile equivalent of openArticle function
   * 
   * @param article - the article to open
   */
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

    let el = document.getElementById("article-container-mobile");
    el.scrollIntoView({
      behavior: 'smooth'
    });
  }

  /**
   * The mobile equivalent of closeArticle function
   */
  closeArticleMobile() {
    var articleDiv = document.getElementById("article-container-mobile");
    articleDiv.style.display = "none";
    articleDiv.style.opacity = "0";

    var articleListDiv = document.getElementById("article-list-mobile");
    articleListDiv.style.display = "flex";
    setTimeout(() => {
      articleListDiv.style.opacity = "1";
    }, 10);
  }

  /**
   * Performs css transition to toggle the filter by date
   * card
   */
  toggleFilter() {
    var mobileFilterDiv = document.getElementById("mobile-filter");

    if (mobileFilterDiv.style.marginRight === "-400px") {
      mobileFilterDiv.style.marginRight = "0";
    } else {
      mobileFilterDiv.style.marginRight = "-400px";
    }
  }

  filterEnter(event){
    event.srcElement.click();
  }

  /**
   * Updates the list of displayed articles to match the selected months/years
   * 
   * @param map - the JSON object containing the list of booleans representing which months/years were selected
   *                (month) list of bool,
   *                (year) list of bool
   */
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
          // Compare with the article's modified_at date or created_at date
          var date = (article.modified_at) ? (new Date(article.modified_at)) : (new Date(article.created_at));
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
          var date = (article.modified_at) ? (new Date(article.modified_at)) : (new Date(article.created_at));
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

  /**
   * Display all visible articles
   */
  seeAll() {
    this.filteredArticles = this.allArticles;
    this.latestArticles = this.allArticles;
  }

  /**
   * Display the most recent articles (the top 8)
   */
  seeMostRecent() {
    this.filteredArticles = this.allArticles.slice(0, 8);
    this.latestArticles = this.allArticles.slice(0, 8);
  }

}
