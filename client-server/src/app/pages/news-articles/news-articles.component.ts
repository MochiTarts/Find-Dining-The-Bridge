import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { faSearch, faStar } from '@fortawesome/free-solid-svg-icons';
import { ArticleService } from '../../_services/article.service';
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-news-articles',
  templateUrl: './news-articles.component.html',
  styleUrls: ['./news-articles.component.scss']
})
export class NewsArticlesComponent implements OnInit {
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
  featuredArticles: any[] = [];

  filterMonthArticles: any[];
  filterYearArticles: any[];

  faSearch = faSearch;
  faStar = faStar;

  selectedArticle: any = Object;
  totalTabs: any[] = [];

  constructor(
    public articleService: ArticleService,
    private userService: UserService,
    private tokenStorage: TokenStorageService,
    private titleService: Title,
    private changeDetection: ChangeDetectorRef,
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

    this.articleService.getArticles().subscribe((data) => {
      // Call endpoint to retrieve articles and set the variables as needed
      //console.log(data.articles)
      this.allArticles = data.articles;
      this.filteredArticles = data.articles;

      this.featuredArticles = this.allArticles.slice(0, 3);
      this.featuredArticles.push(this.featuredArticles[0])
      this.featuredArticles.push(this.featuredArticles[0])

      for (let i = 0; i < this.allArticles.length; i++) {
        this.filteredArticles[i].type = 'article';
      }

      this.selectedArticle = this.filteredArticles[1];
      length = Math.ceil(this.filteredArticles.length/10);
      this.totalTabs = Array(length);
    })
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

  openFilter() {
    var mobileFilterDiv = document.getElementById("mobile-filter");

    if (mobileFilterDiv.style.display === "none") {
      mobileFilterDiv.style.display = "block";
      setTimeout(() => {
        mobileFilterDiv.style.opacity = "0";
        mobileFilterDiv.style.width = "18rem";
      }, 10);
    } else {
      mobileFilterDiv.style.display = "none";
      mobileFilterDiv.style.opacity = "1";
      mobileFilterDiv.style.width = "0";
    }
  }

  filterEnter(event){
    event.srcElement.click();
  }

  filterDate(map) {
    const isFalse = (currentValue) => !currentValue;

    var monthList = map.month;
    var yearList = map.year;

    var monthsFilter = [];
    var yearsFilter = [];

    if (monthList.every(isFalse) && yearList.every(isFalse)) {
      // If every option is unchecked
      this.filteredArticles = this.allArticles;
    } else {
      // If some option(s) are checked
      for (let article of this.allArticles) {
        if (monthList.every(isFalse)) {
          monthsFilter = this.allArticles;
        } else {
          var date = new Date(article.modified_at);
          var monthNumber = date.getMonth();
          for (var i = 0; i < this.months.length; i++) {
            if (monthList[i] && i == monthNumber) {
              monthsFilter.push(article)
            }
          }
        }

        if (yearList.every(isFalse)) {
          yearsFilter = this.allArticles;
        } else {
          var date = new Date(article.modified_at);
          var year = date.getFullYear();
          for (var i = 0; i < this.years.length; i++) {
            if (yearList[i] && this.years[i] == year) {
              yearsFilter.push(article);
            }
          }
        }
      }

      this.filteredArticles = [];
      for (let article of this.allArticles) {
        if (monthsFilter.includes(article) && yearsFilter.includes(article)) {
          this.filteredArticles.push(article);
        }
      }
      
    }
  }

}
