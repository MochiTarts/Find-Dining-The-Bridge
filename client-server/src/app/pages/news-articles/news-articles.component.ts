import { Component, OnInit } from '@angular/core';
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
  displayedArticles: any[];
  featuredArticles: any[];

  filterMonthArticles: any[];
  filterYearArticles: any[];

  faSearch = faSearch;
  faStar = faStar;

  htmlString = '<h1>Hello gowtham</h1><p>This is a string</p>';
  articleContent = "";

  constructor(
    private articleService: ArticleService,
    private userService: UserService,
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

      for (let i = 0; i < this.displayedArticles.length; i++) {
        this.displayedArticles[i].type = 'article';
      }

      this.articleContent = this.displayedArticles[0].content;

      console.log(this.displayedArticles)

      //this.htmlString = data.articles[0].content
    })
  }

  filterEnter(event){
    event.srcElement.click();
  }

  // For filtering by month
  filterMonth(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      // If every option is unchecked
    } else {
      // If some option(s) are checked
    }
  }

  // For filtering by year
  filterYear(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {

    } else {

    }
  }

}
