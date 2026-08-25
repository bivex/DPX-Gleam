import gleam/erlang/process.{type Subject}
import gleam/list
import gleam/otp/actor
import gleam/otp/supervisor
import gleam/otp/task
import gleam/result

pub type ServerMessage {
  CreateUser(email: String, reply_to: Subject(Result(String, String)))
  ListUsers(reply_to: Subject(List(String)))
  Shutdown
}

pub type ServerState {
  ServerState(users: List(String))
}

pub fn handle_message(msg: ServerMessage, state: ServerState) -> actor.Next(ServerMessage, ServerState) {
  case msg {
    Shutdown -> actor.Stop(process.Normal)
    CreateUser(email, reply_to) -> {
      process.send(reply_to, Ok("Created: " <> email))
      let next_state = ServerState(users: [email, ..state.users])
      actor.continue(next_state)
    }
    ListUsers(reply_to) -> {
      process.send(reply_to, state.users)
      actor.continue(state)
    }
  }
}

pub fn start_server() {
  actor.start(ServerState(users: []), handle_message)
}

pub fn start_supervisor() {
  supervisor.start(fn(children) {
    children
    |> supervisor.add(supervisor.worker(start_server))
  })
}

pub fn fetch_remote_metrics() {
  let job = task.async(fn() { [10, 20, 30] })
  task.await(job, 2000)
}
