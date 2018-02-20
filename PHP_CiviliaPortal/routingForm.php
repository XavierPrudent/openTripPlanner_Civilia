<?php
require_once('config/config.php');
require_once('config/db.php');
include('inc/header.php')
?>

<script type="text/javascript" src="res/js/checkRoutingForm.js"></script>

<div class="jumbotron">
    <div class="container">
      <h2 class="display-3"><?php echo PORTAL_NAME?></h2>
      <hr class="my-4">
      <form action="">
        <div class="form-group">
            <label class="control-label col-sm-2">GTFS</label>
            <div class="input-group col-sm-10">
                <input id='gtfs1' class="form-control" type='file' name='gtfs1' onchange="validateGTFSFile()"/>
                <input id='gtfs2' class="form-control" type='file' name='gtfs2'/>
            </div>
            <small class="form-text text-muted col-sm-10">OpenTripPlanner sera lancé avec le premier GTFS</small>
        </div>
        <div class="form-group">
            <label for="select" class="col-sm-2 control-label">Villes</label>
            <div class="col-sm-10">
                <select class="form-control">
                    <option value="none"><?php echo SELECT_CITY_DEFAULT?></option>
                    <option value="Saguenay">Saguenay</option>
                    <option value="Trois-Rivières">Trois-Rivières</option>
                    <option value="Sherbrooke">Sherbrooke</option>
                    <option value="Lévis">Lévis</option>
                </select>
            </div>
        </div>
        <div class="form-group">
            <label class="control-label col-sm-2">Enquête OD</label>
            <div class="input-group col-sm-10">
                <input class="form-control" type='file' name='od-survey' />
            </div>
        </div>

        <div class="form-group">
            <label class="col-sm-2 control-label">Mode de transport</label>
            <div class="col-sm-10">
                <div class="form-control">
                    <div class="form-check">
                        <input id="radioCAR" name="radio-transport-mode" class="form-check-input" checked="" type="radio">
                        <label class="form-check-label" for="radioCAR"> Voiture</label>
                    </div>
                    <div class="form-check">
                        <input id="radioTRANSIT" name="radio-transport-mode" class="form-check-input" type="radio">
                        <label class="form-check-label" for="radioTRANSIT"> Transport en commun</label>
                    </div>
                    <div class="form-check">
                        <input id="radioWALK" name="radio-transport-mode" class="form-check-input" type="radio">
                        <label class="form-check-label" for="radioWALK"> Marche</label>
                    </div>
                </div>
            </div>
        </div>

        <div class="form-group">
          <div class="col-sm-offset-2 col-sm-10">
            <button type="otp" class="btn btn-info btn-lg disabled"><?php echo OTP_BUTTON_TEXT?></button>
            <button type="otp" class="btn btn-info btn-lg disabled"><?php echo STATS_BUTTON_TEXT?></button>
          </div>
        </div>
      </form>
    </div>
</div>


<?php include('inc/footer.php') ?>
