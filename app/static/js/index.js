async function fetchTBA(endpoint) {
  if (endpoint[0] == '/')
    endpoint = endpoint.substring(1);

  const config = {
    method: 'GET',
    headers: {
      'X-TBA-Auth-Key': global.TBA_AUTH_KEY
    }
  }
  const resp = await fetch(`https://www.thebluealliance.com/api/v3/${endpoint}`, config);
  const data = await resp.json();

  return data;
}

async function getEventKey(city) {
  const data = await fetchTBA('/events/2019/simple');
  const eventMatch = data.filter(event => event.city === city);
  
  if (eventMatch.length > 1) {
    console.error(`Conflict when getting event key, two or more events in ${city}.`);
    return;
  }
  else if (eventMatch == 0) {
    console.error(`Unable to find event in ${city}`);
    return;
  }
  // After the checks, there is only one event in the array

  return eventMatch[0].key;
}

async function loadMatchSchedule() {
  const eventKey = await getEventKey(global.CURRENT_EVENT_CITY);

  const allMatches = await fetchTBA(`/event/${eventKey}/matches/simple`);
  const qualificationMatches = allMatches
                                .filter(match => match.comp_level === "qm")
                                .sort((lhs, rhs) => lhs.match_number > rhs.match_number);


  for (match of qualificationMatches) {
    const red = match.alliances.red;
    const blue = match.alliances.blue;
    $('#matchSchedule tbody').append(`
    <tr>
      <th scope="row">${match.match_number}</th>
      <td style="background-color: #ffcccb;">${red.team_keys[0].substring(3)}</td>
      <td style="background-color: #ffcccb;">${red.team_keys[1].substring(3)}</td>
      <td style="background-color: #ffcccb;">${red.team_keys[2].substring(3)}</td>
      <td style="background-color: #add8e6;">${blue.team_keys[0].substring(3)}</td>
      <td style="background-color: #add8e6;">${blue.team_keys[1].substring(3)}</td>
      <td style="background-color: #add8e6;">${blue.team_keys[2].substring(3)}</td>
    </tr>
    `);
  }
}

async function loadRankings() {
  const eventKey = await getEventKey(global.CURRENT_EVENT_CITY);
  
  const data = await fetchTBA(`/event/${eventKey}/rankings`);
  const rankings = data.rankings.map(team => [
    team.rank, // Current Rank
    team.team_key.substring(3), // Team number
    team.extra_stats[0] // Ranking Points
  ]);
  
  return rankings;
}

$(document).ready(() => {
  $('#currentRankings').DataTable({
    paging: true,
    ordering: false,
    lengthChange: false,
    ajax: (data, callback, settings) => loadRankings().then(data => callback({ data: data }))
  })

  loadMatchSchedule()
    .then(_ => {
      // Initialize table after the match schedule is loaded
      $('#matchSchedule').DataTable({
        paging: true,
        ordering: false,
        lengthChange: false
      });
    });
  loadRankings();
});