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
  displayedArticles: any[] = [];
  featuredArticles: any[] = [];
  filteredArticles: any[] = [];

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
      this.displayedArticles = data.articles;

      this.featuredArticles = this.allArticles.slice(0, 3);
      this.featuredArticles.push(this.featuredArticles[0])
      this.featuredArticles.push(this.featuredArticles[0])

      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])
      this.displayedArticles.push(this.displayedArticles[0])

      for (let i = 0; i < this.displayedArticles.length; i++) {
        this.displayedArticles[i].type = 'article';
      }

      this.filteredArticles = this.displayedArticles;

      //this.selectedArticle = this.displayedArticles[0];
      length = Math.ceil(this.displayedArticles.length/10);
      this.totalTabs = Array(length);
      console.log(this.displayedArticles)
    })
  }

  openArticle(article) {
    alert(article.id);
    this.selectedArticle = article;
  }

  filterEnter(event){
    event.srcElement.click();
  }

  // For filtering by month
  filterMonth(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      // If every option is unchecked
      this.filteredArticles = this.allArticles;
    } else {
      // If some option(s) are checked
      this.filteredArticles = [];
      for (let article of this.allArticles) {
        var date = new Date(article.modified_at);
        var monthNumber = date.getMonth();
        for (var i = 0; i < this.months.length; i++) {
          if (list[i] && i == monthNumber) {
            this.filteredArticles.push(article)
          }
        }
      }
    }
  }

  // For filtering by year
  filterYear(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.displayedArticles = this.allArticles;
    } else {
      this.displayedArticles = [];
      for (let article of this.allArticles) {
        var date = new Date(article.modified_at);
        var year = date.getFullYear();
        for (var i = 0; i < this.years.length; i++) {
          if (list[i] && this.years[i] == year) {
            this.displayedArticles.push(article);
          }
        }
      }
    }
  }

}
