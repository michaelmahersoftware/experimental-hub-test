import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { changeExperimentState } from "../../../features/ongoingExperiment";
import {
  getSessionById,
  integerToDateTime,
  useBackListener,
} from "../../../utils/utils";
import Button from "../../atoms/Button/Button";
import Heading from "../../atoms/Heading/Heading";
import Label from "../../atoms/Label/Label";
import LinkButton from "../../atoms/LinkButton/LinkButton";
import TextAreaField from "../TextAreaField/TextAreaField";
import "./OverviewTab.css";

function OverviewTab({
  onLeaveExperiment,
  onStartExperiment,
  onEndExperiment,
}) {
  const [message, setMessage] = useState("");
  const dispatch = useDispatch();
  const ongoingExperiment = useSelector(
    (state) => state.ongoingExperiment.value
  );
  const sessionId = ongoingExperiment.sessionId;
  const sessionsList = useSelector((state) => state.sessionsList.value);
  const sessionData = getSessionById(sessionId, sessionsList)[0];

  useBackListener(() => onLeaveExperiment());

  const onEnterMessage = (newMessage) => {
    setMessage(newMessage);
  };

  const onStopExperiment = () => {
    dispatch(changeExperimentState("WAITING"));
    onEndExperiment();
  };

  console.log("experimentState", ongoingExperiment.experimentState);

  return (
    <div className="overviewTabContainer">
      <Heading heading={sessionData.title} />
      <hr className="separatorLine"></hr>
      <div className="sessionInformation">
        <h3>Session Information</h3>
        <div className="sessionDuration">
          <div>
            <Label title={"Time Limit: "} /> {sessionData.time_limit / 60000}
          </div>
          <div>
            <Label title={"Starting time: "} />
            {sessionData.start_time > 0
              ? integerToDateTime(sessionData.start_time)
              : "Not started yet"}
          </div>
          <div>
            <Label title={"Ending time: "} />{" "}
            {sessionData.end_time > 0
              ? integerToDateTime(sessionData.start_time)
              : "Not ended yet"}
          </div>
        </div>
        <hr className="separatorLine"></hr>
      </div>
      <div className="sessionInformation">
        <h3>Send Message to all participants</h3>
        <TextAreaField
          placeholder={"Enter your message here"}
          value={message}
          onChange={(newMessage) => onEnterMessage(newMessage)}
        />
        <Button name={"Send"} design={"secondary"} />
      </div>
      <hr className="separatorLine"></hr>

      <LinkButton
        name={"LEAVE EXPERIMENT"}
        design={"secondary"}
        to={"/"}
        onClick={() => onLeaveExperiment()}
      />
      {ongoingExperiment.experimentState === "WAITING" ? (
        <Button
          name={"START EXPERIMENT"}
          design={"positive"}
          onClick={() => onStartExperiment()}
        />
      ) : (
        <LinkButton
          name={"END EXPERIMENT"}
          design={"negative"}
          to="/"
          onClick={() => onStopExperiment()}
        />
      )}
    </div>
  );
}

export default OverviewTab;
