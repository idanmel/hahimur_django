# Hahimur-Django
Backend for Hahimur, which is a site for my friends and I to predict
major football tournament games.

## Authorization
Every User has a token, and should be passed as a query parameter
```bash
https://live-site.com/tournaments/1/predictions?token=<token>
```

## API Endpoints
```bash
POST    '/tournaments/<int>/predictions'
```


#### POST '/tournaments'
The post request should have a json body containing all the group matches, 
knockout matches and top_scorer.
like so:
```json
{
   "group_matches": [
      { 
        "match_number": 1, 
        "home_score": 2, 
        "away_score": 0
      }
  ],
  "knockout_matches": [
      { 
        "match_number": 2, 
        "home_score": 1, 
        "away_score": 1,
        "home_win": true
      }
  ],
  "top_scorer": "Villa"
 
}
```