
def run(discussion, on_chunk_callback):
    # This script overrides the normal chat flow.
    user_message = discussion.get_branch(discussion.active_branch_id)[-1].content
    response = f"Squawk! {user_message}! Squawk!"
    if on_chunk_callback:
        # We need to simulate the message type for the callback
        from lollms_client import MSG_TYPE
        on_chunk_callback(response, MSG_TYPE.MSG_TYPE_CHUNK)
    return response # Return the full raw response
