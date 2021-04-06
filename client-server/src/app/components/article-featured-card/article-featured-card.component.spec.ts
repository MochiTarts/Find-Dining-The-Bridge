import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleFeaturedCardComponent } from './article-featured-card.component';

describe('ArticleFeaturedCardComponent', () => {
  let component: ArticleFeaturedCardComponent;
  let fixture: ComponentFixture<ArticleFeaturedCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleFeaturedCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleFeaturedCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
