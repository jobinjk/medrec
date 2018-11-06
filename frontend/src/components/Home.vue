<template>
  <v-container fluid grid-list-lg>
    <!-- Headers -->
    <div>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card tile flat>
            <v-card-text>
              <v-layout row wrap>
                <v-flex xs12>
                  <p class="headline">Home</p>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </div>

    <!-- Filters and search -->
    <div>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card tile flat>
            <!-- Add search and filter here -->
            <v-spacer></v-spacer>

          <v-flex xs6>
            <v-text-field name="Enter patient id" v-model="search"></v-text-field>
            <v-btn color="teal" @click.native="fetchPatient()">Search</v-btn>
          </v-flex>
          </v-card>
        </v-flex>
      </v-layout>
    </div>

    <!-- Content -->

    <v-layout row wrap>
      <v-flex xs4 v-if="patient.id">
        <v-card color="grey lighten-4" class="elevation-7">
          <v-card-title class="headline blue-grey--text">
            {{patient.name}}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <span class="caption"><u>Patient ID:</u><br>
              <strong class="subheading blue-grey--text">{{patient.id}}</strong>
            </span>
            <v-flex xs5>
                  <v-img
                    :src= 'origin+"/qr_images/patient_"+patient.id+".png"'
                    height="125px"
                    contain
                  ></v-img>
            </v-flex>
            <br>
            <span class="caption">
              <label><u>Description</u></label><br>
              {{patient.description}}
            </span>
            <br>
            <span class="caption">
              <label><u>Medication</u></label><br>
              <v-chip v-for="(med,index) in patient.medication" :key="index" color="deep-purple darken-1" outline dark label>{{med}}</v-chip>
            </span>
            <br>
            <span class="caption">
              <label><u>Doctor's Name</u></label><br>
              {{patient.added_by["username"]}}
            </span>
            <br>
            <v-tooltip top>
              <span slot="activator" class="grey--text">Created on:- {{  patient.created_on | humanizeTime}}</span>
              <span> {{ patient.created_on | calendarTime}} </span>
            </v-tooltip>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn icon @click.stop="editPatientView=true; editPatient=patient;buildEditMedications(patient); error = {status:false,text:''}">
              <v-icon color="amber darken-1">fa-edit</v-icon>
            </v-btn>
            <v-btn icon @click.native="deletePatient(patient.id)">
              <v-icon color="error darken-1">fa-trash</v-icon>
            </v-btn> 
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>

     <!-- Edit Patient form modal -->

      <v-layout row justify-center>
        <v-dialog v-model="editPatientView" persistent max-width="890" >
          <v-card>
            <v-card-title class="headline">Edit Patient</v-card-title>
            <v-card-text>You can edit a Patient here. </v-card-text>
            <v-card-text>
              <v-form v-model="editPatientForm" ref="editPatientForm" @submit.prevent="updatePatient" >
                <v-layout row wrap>
                  <v-flex xs12>
                    <v-text-field solo dark name="name" label="Name" placeholder="Enter Patients Name" id="name" v-model="editPatient.name" required></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field solo dark name="description" label="Description" placeholder="Enter Patients Description" id="description" v-model="editPatient.description" required></v-text-field>

                  </v-flex>
                  <v-flex xs12 v-for="(med,index) in editPatientMedication" :key="index">
                    <v-layout row wrap>
                      <v-flex xs11>
                        <v-text-field dark name="medication" solo label="Medication" placeholder="Enter Patients Medication" id="medication" v-model="med.patient" required></v-text-field>
                      </v-flex>
                      <v-flex xs1>
                        <v-btn color="error" dark icon small @click.native="editPatientMedication.splice(index,1)">
                          <v-icon small>delete</v-icon>
                        </v-btn>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                  <v-btn color="teal" dark small @click.native="editPatientMedication.push({patient:''})">
                    <v-icon>add</v-icon>&nbsp; Add medication
                  </v-btn>
                </v-layout>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="error darken-1" flat @click.native="editPatient.meds=[];editPatientView = false;">Cancel</v-btn>
                  <v-btn color="success darken-1" flat type="submit">Save</v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-layout>



    
    </v-container>


  </template>
  <script>
    export default {
      name: 'Home',
      props: {
        wid: {
          type: String,
          default: null
        }
      },
      computed:{
        origin:function(){
          return process.env.BASE_ORIGIN
        }
      },
      data () {
        return {
           patient: {
            name: '',
            description: '',
            medication: '',
            added_by: '',
            created_on: ''
           },
           search:'',
           editPatientView: false,
           editPatientForm: false,
           editPatientMedication: [],
           editPatient: {
            name: '',
            description: '',
            medication: [],
            patients:[],

            meds:[{patient:''}]
          },          
        }
      },
      methods: {
        fetchPatient () {
        this.patient={}
        var url = '/api/search?id='+this.search
        this.$http.get(url).then(
          (response) => {
            this.patient = response.data
          },
          (err) => {
            this.patient.loading = false
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Patient fetching failed!!!'
            })
          })
      },

      buildEditMedications(item){
        this.editPatientMedication = []
        for (var i = item.medication.length - 1; i >= 0; i--) {
          this.editPatientMedication.push({item:item.medication[i]})
        }
      },
      updatePatient () {
        this.editPatient.medication = []
        for (var i = this.editPatientMedication.length - 1; i >= 0; i--) {
          this.editPatient.medication.push(this.editPatientMedication[i].item)          
        }
        var url = '/api/patients/' + this.editPatient.id
        this.$http.put(url, this.editPatient).then(
          (response) => {
            if (response.status === 200){
              this.editPatientView = false
              this.$refs.editPatientForm.reset()
              this.editPatientMedication = [{item:''}]
              this.fetchPatient(1)
              this.$notify({
                title: response.statusText,
                type: 'success',
                text: 'Hello, the Patient is editted successfully!!!'
              })
            }
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Hello, the Patient editting failed!!!'
            })
          })
      },
      deletePatient (pid) {
        var url = '/api/patients/' + pid
        this.$http.delete(url).then(
          (response) => {
            if (response.status === 200) {
              this.fetchPatient()
              this.$notify({
                title: 'Patient Deleted',
                type: 'warn',
                text: 'Hello, the patient is deleted successfully!!!'
              })
            }
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Hello, the patient deleting failed!!!'
            }.bind(this))
          })
      }

    },
    created() {
      // this.fetchPatient()
    }
  }

</script>
