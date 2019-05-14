public GameObject paint;

void update(){
	if(Input.GetMouseButton(2)){
	Instantiate(paint, transform.position, transform.rotation);
	}
}